from hub_pip.api.model.CodeLocationView import CodeLocationView


class PagedCodeLocationView(object):

    total_count = None
    items = None

    attribute_map = {
        "total_count": "totalCount",
        "items": "items",
    }

    attribute_schema = {
        "items": [CodeLocationView]
    }

    def __init__(self):
        pass
