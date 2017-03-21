import json


def from_json_file(json_file, cls):
    json_ = json_file.read()
    return map_to_object(json_, cls)


def from_json_string(json_string, cls):
    json = json.loads(json_string)
    return map_to_object(json, cls)


def map_to_object(data, cls):  # data is a dictionary. cls is the class to convert to
    obj = cls()
    for k, v in data.items():
        key = __exhange__(obj, k, to_left=True)
        setattr(obj, key, v)
    return obj


def map_from_object(obj):
    dictionary = {}
    attr_map = obj.attribute_map
    for k, v in attr_map.items():
        dictionary[v] = getattr(obj, k)
    return dictionary


def __exhange__(obj, key, to_left=True):
    """Exchange provided key for mapped version"""
    if hasattr(obj, "attribute_map"):
        for k, v in obj.attribute_map.items():
            if to_left and v == key:
                return k
            elif not to_left and k == key:
                return v

    else:
        print(obj + " does not contain the attribute_map dictionary attribute")
        return None
    return key  # No match was found. Keep the same
