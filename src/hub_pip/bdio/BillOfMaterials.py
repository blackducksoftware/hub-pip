import uuid


class BillOfMaterials(object):

    id = None
    type = None
    name = None
    external_id = None
    relationships = None
    spec_version = None

    attribute_map = {
        "id": "@id",
        "type": "@type",
        "name": "spdx:name",
        "external_id": "externalIdentifier",
        "relationships": "relationship",
        "spec_version": "spec_version"
    }

    def __init__(self):
        self.id = "uuid:" + str(uuid.uuid4())
        self.type = "BillOfMaterials"
        self.spec_version = "1.1.0"

    def __eq__(self, other):
        if isinstance(other, BillOfMaterials):
            type = self.type == other.type
            name = self.name = other.name
            external_id = self.external_id == other.external_id
            spec_version = self.spec_version == other.spec_version
            relationships = True
            if self.relationships is not None and other.relationships is not None:
                relationships = len(self.relationships) == len(
                    other.relationships)
                if relationships:
                    for relationship in self.relationships:
                        if not relationship in other.relationships:
                            relationships = False
                            break
            elif self.relationships != other.relationships:
                # One is set to None
                relationships = False
            return (type and name and external_id and spec_version and relationships)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
