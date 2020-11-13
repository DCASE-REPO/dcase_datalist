#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import glob
import yaml
import json


def main(argv):
    print('Updating JSON files')
    print('===================')

    # Target files
    scenes_list = os.path.join('lists', 'dcase_scenes_datasets.json')
    events_list = os.path.join('lists', 'dcase_events_datasets.json')
    captions_list = os.path.join('lists', 'dcase_captions_datasets.json')

    # Paths
    dataset_meta_path = 'datasets'
    scenes_dataset_meta_path = os.path.join(dataset_meta_path, 'scenes')
    events_dataset_meta_path = os.path.join(dataset_meta_path, 'events')
    captions_dataset_meta_path = os.path.join(dataset_meta_path, 'captions')

    # File lists
    scenes_dataset_meta_files = glob.glob(scenes_dataset_meta_path + "/*.yaml")
    events_dataset_meta_files = glob.glob(events_dataset_meta_path + "/*.yaml")
    captions_dataset_meta_files = glob.glob(captions_dataset_meta_path + "/*.yaml")

    # Read template
    scenes_template_filename = os.path.join(dataset_meta_path, 'scenes_template.yaml')
    with open(scenes_template_filename, 'r') as file:
        scenes_template = yaml.load(file, Loader=yaml.FullLoader)

    events_template_filename = os.path.join(dataset_meta_path, 'events_template.yaml')
    with open(events_template_filename, 'r') as file:
        events_template = yaml.load(file, Loader=yaml.FullLoader)

    captions_template_filename = os.path.join(dataset_meta_path, 'captions_template.yaml')
    with open(events_template_filename, 'r') as file:
        captions_template = yaml.load(file, Loader=yaml.FullLoader)

    # Classification datasets
    scenes_list_data = []
    for dataset_meta_file in scenes_dataset_meta_files:
        with open(dataset_meta_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            item = {}

            for key1 in list(scenes_template.keys()):
                if isinstance(scenes_template[key1], dict):
                    for key2 in list(scenes_template[key1].keys()):
                        if isinstance(scenes_template[key1][key2], dict):
                            for key3 in list(scenes_template[key1][key2].keys()):
                                item[key1 + '-' + key2+'-'+key3] = data.get(key1, {}).get(key2, {}).get(key3, None)
                        else:
                            if data.get(key1, None):
                                item[key1+'-'+key2] = data.get(key1, {}).get(key2, None)
                            else:
                                item[key1 + '-' + key2] = None
                else:
                    item[key1] = data.get(key1, None)

            scenes_list_data.append(item)

    # Detection datasets
    events_list_data = []
    for dataset_meta_file in events_dataset_meta_files:
        with open(dataset_meta_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            item = {}

            for key1 in list(events_template.keys()):
                if isinstance(events_template[key1], dict):
                    for key2 in list(events_template[key1].keys()):
                        if isinstance(events_template[key1][key2], dict):
                            for key3 in list(events_template[key1][key2].keys()):
                                if isinstance(events_template[key1][key2][key3], dict):
                                    for key4 in list(events_template[key1][key2][key3].keys()):
                                        item[key1 + '-' + key2 + '-' + key3 + '-' + key4] = data.get(key1, {}).get(key2, {}).get(key3, {}).get(key4, None)
                                else:
                                    item[key1 + '-' + key2+'-'+key3] = data.get(key1, {}).get(key2, {}).get(key3, None)
                        else:
                            if data.get(key1, None):
                                item[key1+'-'+key2] = data.get(key1, {}).get(key2, None)
                            else:
                                item[key1 + '-' + key2] = None
                else:
                    item[key1] = data.get(key1, None)

            for field in list(item.keys()):
                if item[field] is None:
                    item[field] = ''

            events_list_data.append(item)

    # Captions datasets
    captions_list_data = []

    # store files
    with open(scenes_list, 'w') as outfile:
        json.dump(scenes_list_data, outfile)

    with open(events_list, 'w') as outfile:
        json.dump(events_list_data, outfile)

    with open(captions_list, 'w') as outfile:
        json.dump(captions_list_data, outfile)

    print('  [DONE]')

if __name__ == "__main__":
    sys.exit(main(sys.argv))