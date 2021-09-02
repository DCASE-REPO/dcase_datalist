#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import glob
import yaml
import json


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
                    print('   ', data['dataset']['name'])
                    item = process_dataset_meta(data, template)
                    list_data.append(item)
                    if item['dataset-name'] not in global_list_data:
                        global_list_data[item['dataset-name']] = item
                    else:
                        global_list_data[item['dataset-name']].update(item)
                else:
                    print('    [SKIPPED]', data['dataset']['name'])

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


if __name__ == "__main__":
    sys.exit(main(sys.argv))