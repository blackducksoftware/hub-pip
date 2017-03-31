import uuid


class BillOfMaterials(object):

    id_ = None
    type_ = None
    name = None
    external_id = None
    relationships = None
    specVersion = None

    attribute_map = {
        "id_": "@id",
        "type_": "@type",
        "name": "spdx:name",
        "external_id": "externalIdentifier",
        "relationships": "relationship",
        "specVersion": "specVersion"
    }

    def __init__(self):
        self.id_ = "uuid:" + str(uuid.uuid4())
        self.type_ = "BillOfMaterials"
        self.specVersion = "1.1.0"
