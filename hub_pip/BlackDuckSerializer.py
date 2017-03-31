import inspect
import json


def from_json_file(json_file, cls):
    json_ = json_file.read()
    return from_json_string(json_, cls)


def from_json_string(json_string, cls):
    json = json.loads(json_string)
    return map_to_object(json, cls)


def map_to_object(data, cls):  # data is a dictionary. cls is the class to convert to
    obj = cls()
    if data:
        for k, v in data.items():
            key = _exhange(obj, k)
            if key:
                setattr(obj, key, v)
        _exhange_properties(obj)
    return obj


def map_from_object(obj):
    dictionary = {}
    attr_map = obj.attribute_map
    for k, v in attr_map.items():
        attr = getattr(obj, k)
        if attr:
            dictionary[v] = attr
    return dictionary


def _exhange(obj, key):
    """Exchange provided key for mapped version"""
    if hasattr(obj, "attribute_map"):
        for k, v in obj.attribute_map.items():
            if v == key:
                return k
    return None


def _exhange_properties(obj):
    """Exchange provided key for schema class"""
    if hasattr(obj, "attribute_schema"):
        for k, v in obj.attribute_schema.items():
            data = None
            if isinstance(v, list) and v[0]:
                if inspect.isclass(v[0]):
                    data = [map_to_object(item, v[0])
                            for item in getattr(obj, k)]
                    setattr(obj, k, data)
            elif inspect.isclass(v):
                data = map_to_object(getattr(obj, k), v)
                setattr(obj, k, data)
            else:
                raise Exception(
                    "Value of attribute_schema is not a class or list of a single class")
    return None
