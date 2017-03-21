class BillOfMaterials(object):

    id_ = None
    type_ = None
    name = None
    external_identifier = None
    relationships = None
    bdio_specification_version = None

    attribute_map = {
        "id_": "@id",
        "type_": "@type",
        "name": "name",
        "external_identifier": "externalIdentifier",
        "relationships": "relationship",
        "bdio_specification_version": "specVersion"
    }

    def __init__(self):
        type_ = "BillOfMaterials"
