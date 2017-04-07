from hub_pip.api.model.MetadataView import MetadataView


class CodeLocationView(object):

    created_at = None
    mapped_project_version = None
    type = None
    updated_at = None
    url = None
    metadata = None

    attribute_map = {
        "created_at": "createdAt",
        "mapped_project_version": "mappedProjectVersion",
        "type": "type",
        "updated_at": "updatedAt",
        "url": "url",
        "metadata": "_meta"
    }

    attribute_schema = {
        "metadata": MetadataView
    }

    def __init__(self):
        pass
