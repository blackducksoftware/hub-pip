class BdioProject(object):

    id_ = None
    type_ = "Project"
    name = None
    external_id = None
    relationships = None
    version = None

    attribute_map = {
        "id_": "@id",
        "type_": "@type",
        "name": "name",
        "external_id": "externalIdentifier",
        "relationships": "relationship",
        "version": "revision"
    }

    def __init__(self):
        pass
