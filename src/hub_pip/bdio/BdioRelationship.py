class BdioRelationship(object):

    related = None
    relationship_type = "DYNAMIC_LINK"

    attribute_map = {
        "related": "related",
        "relationship_type": "relationshipType",
    }

    def __init__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, BillOfMaterials):
            related = self.related == other.related
            relationship_type = self.relationship_type == other.relationship_type
            return (related and relationship_type)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)