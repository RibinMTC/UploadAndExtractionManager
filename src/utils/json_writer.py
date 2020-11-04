import json


def get_dict_from_json(json_path):
    with open(json_path, 'r') as json_file:
        json_dict = json.load(json_file)
    return json_dict


def store_dict_to_json(json_path, json_dict):
    with open(json_path, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)
