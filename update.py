#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import glob
import yaml
import json
from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

def process_dataset_meta(data, template):
    item = {}
    for key1 in list(template.keys()):
        if isinstance(template[key1], dict):
            for key2 in list(template[key1].keys()):
                if isinstance(template[key1][key2], dict):
                    for key3 in list(template[key1][key2].keys()):
                        if isinstance(template[key1][key2][key3], dict):
                            for key4 in list(template[key1][key2][key3].keys()):
                                item[key1 + '-' + key2 + '-' + key3 + '-' + key4] = data.get(key1, {}).get(key2, {}).get(key3, {}).get(key4, None)
                        else:
                            item[key1 + '-' + key2 + '-' + key3] = data.get(key1, {}).get(key2, {}).get(key3, None)
                else:
                    if data.get(key1, None):
                        item[key1 + '-' + key2] = data.get(key1, {}).get(key2, None)
                    else:
                        item[key1 + '-' + key2] = None
        else:
            item[key1] = data.get(key1, None)

    for field in list(item.keys()):
        if item[field] is None:
            item[field] = ''

    return item


def main(argv):
    print('Updating JSON files')
    print('===================')

    template_files = []
    for file in os.listdir('datasets'):
        if file.endswith('_template.yaml'):
            template_files.append(os.path.join('datasets', file))

    item_template_files = []
    for file in os.listdir('templates'):
        if file.endswith('_template.html'):
            item_template_files.append(file)

    all_data = {}
    for item_template_file in item_template_files:
        category_label = os.path.split(item_template_file)[-1].split('_')[0]
        if category_label not in all_data:
            all_data[category_label] = {}

        dataset_meta_path = os.path.join('datasets', category_label)
        dataset_meta_files = glob.glob(dataset_meta_path + "/*.yaml")
        for dataset_meta_file in dataset_meta_files:
            with open(dataset_meta_file, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                data['dataset_meta_file'] = dataset_meta_file
                if data['dataset']['abbreviation'] not in all_data[category_label]:
                    data['item_html_filename'] = os.path.join('datasets', category_label, os.path.splitext(os.path.split(dataset_meta_file)[-1])[0] + '.html')
                    data['item_link_html'] = '<a class="btn2 btn-success2" href="'+data['item_html_filename']+'" title="Item information page for ['+data['dataset']['name']+']"><i class="fa fa-arrow-circle-right fa-3x icon-color-active2" aria-hidden="true"></i></a>'

                    data['item_html_filename2'] = os.path.join(category_label, os.path.splitext(os.path.split(dataset_meta_file)[-1])[0] + '.html')
                    data['item_link_html2'] = '<a class="btn2 btn-success2" href="' + data['item_html_filename2'] + '" title="Item information page for [' + data['dataset']['name'] + ']"><i class="fa fa-arrow-circle-right fa-3x icon-color-active2" aria-hidden="true"></i></a>'

                    data['dataset_id'] = os.path.join(category_label, os.path.splitext(os.path.split(dataset_meta_file)[-1])[0])

                    all_data[category_label][data['dataset']['abbreviation']] = data

    global_list_data = {}
    for template_file in template_files:
        category_label = os.path.split(template_file)[-1].split('_')[0]
        print(' ', category_label)

        # Read template
        with open(template_file, 'r') as file:
            template = yaml.load(file, Loader=yaml.FullLoader)

        dataset_meta_path = os.path.join('datasets', category_label)
        dataset_meta_files = glob.glob(dataset_meta_path + "/*.yaml")

        # Process datasets
        list_data = []
        for dataset_meta_file in dataset_meta_files:
            with open(dataset_meta_file, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                if 'skip' not in data or data['skip'] == False:
                    print('   ', dataset_meta_file)

                    item = process_dataset_meta(data, template)

                    if category_label in all_data and data['dataset']['abbreviation'] in all_data[category_label]:
                        item['item_link_html'] = all_data[category_label][data['dataset']['abbreviation']]['item_link_html']
                        item['item_html_filename'] = all_data[category_label][data['dataset']['abbreviation']]['item_html_filename']
                        item['dataset-id'] = os.path.join(category_label, os.path.splitext(os.path.split(dataset_meta_file)[-1])[0])

                    list_data.append(item)
                    if item['dataset-name'] not in global_list_data:
                        global_list_data[item['dataset-name']] = item
                    else:
                        global_list_data[item['dataset-name']].update(item)
                else:
                    print('    [SKIPPED]', dataset_meta_file)

        # Target
        list_filename = os.path.join('docs', 'datasets_' + category_label + '.json')

        with open(list_filename, 'w') as outfile:
            json.dump(list_data, outfile)

        print('    ====================================')
        print('    SAVED [', list_filename, ']')
        print(' ')

    # Target
    global_list_filename = os.path.join('docs', 'datasets.json')
    with open(global_list_filename, 'w') as outfile:
        json.dump(list(global_list_data.values()), outfile)
    print('  ====================================')
    print('  SAVED [', global_list_filename, ']')
    print(' ')
    print('  [DONE]')

    print(' ')
    print('Updating dataset specific pages')
    print('===================')

    if not os.path.exists(os.path.join('docs', 'datasets')):
        os.makedirs(os.path.join('docs', 'datasets'))

    env = Environment()
    env.loader = FileSystemLoader('templates')

    for item_template_file in item_template_files:
        category_label = os.path.split(item_template_file)[-1].split('_')[0]
        print(' ', category_label)

        if not os.path.exists(os.path.join('docs', 'datasets', category_label)):
            os.makedirs(os.path.join('docs', 'datasets', category_label))

        jinja_template = env.get_template(item_template_file)

        dataset_meta_path = os.path.join('datasets', category_label)
        dataset_meta_files = glob.glob(dataset_meta_path + "/*.yaml")

        # Process datasets
        for dataset_meta_file in dataset_meta_files:
            print('   ', dataset_meta_file)

            with open(dataset_meta_file, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                if 'skip' not in data or data['skip'] is False:
                    data['category_label'] = category_label

                    if 'related_datasets' in data['dataset'] and data['dataset']['related_datasets']:
                        rel_list = []
                        for rel in data['dataset']['related_datasets']:

                            if rel in all_data[category_label]:
                                rel_list.append(
                                    {
                                        'title': rel,
                                        'url': '../../'+all_data[category_label][rel]['item_html_filename']
                                    }
                                )
                            else:
                                found = False
                                for cat in all_data:
                                    if rel in all_data[cat]:
                                        rel_list.append(
                                            {
                                                'title': rel,
                                                'url': '../../' + all_data[cat][rel]['item_html_filename']
                                            }
                                        )
                                        found = True
                                        break
                                if not found:
                                    rel_list.append(
                                        {
                                            'title': rel
                                        }
                                    )

                        data['dataset']['related_datasets_linked'] = rel_list

                    data['dataset']['id'] = os.path.join(category_label, os.path.splitext(os.path.split(dataset_meta_file)[-1])[0])

                    dataset_item_html_filename = os.path.join('docs', 'datasets', category_label, os.path.splitext(os.path.split(dataset_meta_file)[-1])[0] + '.html')

                    # to save the results
                    with open(dataset_item_html_filename, "w") as fh:
                        item_rendered = jinja_template.render(**data)
                        fh.write(item_rendered)
        print(' ')

        print('Updating index page for datasets')
        print('===================')
        jinja_template = env.get_template('item_list.html')

        for category_label in all_data:
            for item in all_data[category_label]:
                print('   ', '['+category_label+']', all_data[category_label][item]['dataset_meta_file'])

        html_filename = os.path.join('docs', 'datasets', 'list.html')

        # to save the results
        with open(html_filename, "w") as fh:
            item_rendered = jinja_template.render(data=all_data)
            fh.write(item_rendered)


if __name__ == "__main__":
    sys.exit(main(sys.argv))