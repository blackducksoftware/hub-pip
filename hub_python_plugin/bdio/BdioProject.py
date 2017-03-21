class BdioProject(object):

    id_ = None
    type_ = None
    name = None
    external_identifier = None
    relationships = None

    attribute_map = {
        "id_": "@id",
        "type_": "@type",
        "name": "name",
        "external_identifier": "externalIdentifier",
        "relationships": "relationship",
    }

    def __init__(self):
        type_ = "Project"
