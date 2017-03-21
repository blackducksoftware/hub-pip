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
        key = __exhange__(obj, k)
        if key:
            setattr(obj, key, v)
    return obj


def map_from_object(obj):
    dictionary = {}
    attr_map = obj.attribute_map
    for k, v in attr_map.items():
        dictionary[v] = getattr(obj, k)
    return dictionary


def __exhange__(obj, key):
    """Exchange provided key for mapped version"""
    if hasattr(obj, "attribute_map"):
        for k, v in obj.attribute_map.items():
            if v == key:
                return k
    else:
        print(obj + " does not contain the attribute_map dictionary attribute")
    return None
    # return key  # No match was found. Keep the same


data = {
    "@id": "1234567890",
    "@type": "ComponentTest",
    "name": "six",
    "externalIdentifier": "pypi:six/1.10.0",
    "relationships": []
}
