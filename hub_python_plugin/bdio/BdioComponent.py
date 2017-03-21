class BdioComponent(object):

    id_ = None
    type_ = None
    name = None
    external_identifier = None
    relationships = None
    version = None

    attribute_map = {
        "id_": "@id",
        "type_": "@type",
        "name": "name",
        "external_identifier": "externalIdentifier",
        "relationships": "relationship",
        "version": "revision"
    }

    def __init__(self):
        type_ = "Component"
