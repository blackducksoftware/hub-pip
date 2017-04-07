from hub_pip.api.model.ProjectView import ProjectView


class PagedProjectView(object):

    total_count = None
    items = None

    attribute_map = {
        "total_count": "totalCount",
        "items": "items",
    }

    attribute_schema = {
        "items": [ProjectView]
    }

    def __init__(self):
        pass
