class BdioComponent(object):

    id = None
    type = "Component"
    name = None
    external_id = None
    relationships = None
    version = None

    attribute_map = {
        "id": "@id",
        "type": "@type",
        "name": "name",
        "external_id": "externalIdentifier",
        "relationships": "relationship",
        "version": "revision"
    }

    def __init__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, BdioComponent):
            id = self.id == other.id
            type = self.type == other.type
            name = self.name == other.name
            external_id = self.external_id == other.external_id
            version = self.version == other.version
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
            return (id and type and name and external_id and version and relationships)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)