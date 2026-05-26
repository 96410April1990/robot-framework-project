import json
from jsondiff import diff

listOfDicts = []
unavailable_objects = []

def get_json_keys(json_obj, result=None):
    if result is None:
        result = []
    if isinstance(json_obj, dict):
        for key in json_obj:
            result.append(key)
            get_json_keys(json_obj[key], result)
    elif isinstance(json_obj, list):
        for item in json_obj:
            get_json_keys(item, result)
    return result
    
def compare_jsons(jsonOne, jsonTwo):
    getDiff = diff(jsonOne, jsonTwo)
    getDiffJson = json.dumps(getDiff)
    return getDiffJson      

def iterate_json_and_check_keys(json_one, json_two):
    json_one_keys = set(find_missing_keys(json_one))
    json_two_keys = set(find_missing_keys(json_two))
    unavailable_objects_set = json_one_keys - json_two_keys
    unavailable_objects = list(unavailable_objects_set)
    return unavailable_objects
    
def find_missing_keys(json_obj):
    for k, v in json_obj.items():
        yield k
        if isinstance(v, dict):
            for child_key in find_missing_keys(v):
                yield child_key
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    for child_key in find_missing_keys(item):
                        yield child_key


def parse_json(json_obj, language, parent_key=""):
    with open('./PDFDataExtraction/PageObjects/pdf_objects_section_six_merged_json_'+language+'.json') as file:
        section_six_verbiage = json.load(file)
    for key, value in json_obj.items():
        new_key = f"{parent_key}.{key}"
        if isinstance(value, dict):
            parse_json(value, language, new_key)
        else:
            print(f"Parent: {parent_key}, Key: {key}, Value: {value}")
            if parent_key.startswith('.'):
                parent_key = parent_key[1:]
            
            value = str(value)
            if value.startswith('[') and value.endswith(']'):
                value = value[1:-1]
                if value.startswith('\'') and value.endswith('\''):
                    value = value[1:-1]

            getVerbiage = section_six_verbiage[key]
            if '?' in getVerbiage:
                getVerbiage = getVerbiage.replace('?', ' ')

            createDict = {
                "Parent Key": parent_key,
                "Key": key,
                "DRM Verbiage": getVerbiage,
                "Value": value
            }
            listOfDicts.append(createDict)
    return listOfDicts