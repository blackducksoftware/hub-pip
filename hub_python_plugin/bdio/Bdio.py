from BdioComponent import BdioComponent
from BdioExternalIdentifier import BdioExternalIdentifier
from BdioProject import BdioProject
from BdioRelationship import BdioRelationship
from BillOfMaterials import BillOfMaterials
from hub_python_plugin.Package import Package

class Bdio(object):

    tree = None

    def __init__(self, tree):
        self.tree = tree

    def generate_bdio(self):
        return []
