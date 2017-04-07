from hub_pip.api.model.MetadataView import MetadataView


class ProjectView(object):

    description = None
    name = None
    project_level_adjustments = None
    project_tier = None
    source = None
    metadata = None

    attribute_map = {
        "description": "description",
        "name": "name",
        "project_level_adjustments": "projectLevelAdjustments",
        "project_tier": "projectTier",
        "source": "source",
        "metadata": "_meta"
    }

    attribute_schema = {
        "metadata": MetadataView
    }

    def __init__(self):
        pass
