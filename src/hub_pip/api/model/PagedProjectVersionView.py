from hub_pip.api.model.ProjectVersionView import ProjectVersionView


class PagedProjectVersionView(object):

    total_count = None
    items = None

    attribute_map = {
        "total_count": "totalCount",
        "items": "items",
    }

    attribute_schema = {
        "items": [ProjectVersionView]
    }

    def __init__(self):
        pass
