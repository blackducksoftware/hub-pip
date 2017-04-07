
from hub_pip.BlackDuckPackage import BlackDuckPackage
from hub_pip.BlackDuckSerializer import *
from hub_pip.FileHandler import *
from hub_pip.TreeHandler import TreeHandler
from hub_pip.bdio.BdioComponent import BdioComponent
from hub_pip.bdio.BdioExternalIdentifier import BdioExternalIdentifier
from hub_pip.bdio.BdioProject import BdioProject
from hub_pip.bdio.BdioRelationship import BdioRelationship
from hub_pip.bdio.BillOfMaterials import BillOfMaterials


class Bdio(object):

    tree = None
    code_location_name = None

    def __init__(self, tree, code_location_name):
        self.tree = tree
        self.code_location_name = code_location_name
        if self.code_location_name is None:
            self.code_location_name = tree.name + "/" + \
                tree.version + " Black Duck I/O Export"

    def generate_bdio(self):
        bdio = []
        bom = self._get_bom()
        project = self._get_node(BdioProject(), self.tree)
        components = self._get_components()

        bdio.append(bom)
        bdio.append(project)
        bdio.extend(components)
        return bdio

    def _get_bom(self):
        bom = BillOfMaterials()
        bom.name = self.code_location_name
        bom = map_from_object(bom)
        return bom

    def _get_node(self, node, package):
        node.id = package.get_internal_id()
        node.name = package.name
        node.version = package.version
        node.relationships = self._get_relationships(package)
        node.external_id = map_from_object(package.get_external_id())
        node = map_from_object(node)
        return node

    def _get_components(self):
        components = self.tree.flatten()
        components = [self._get_node(BdioComponent(), pkg)
                      for pkg in components]
        return components

    def _get_relationships(self, package):
        relationships = []
        for pkg in package.dependencies:
            relationship = BdioRelationship()
            relationship.related = pkg.get_internal_id()
            relationship = map_from_object(relationship)
            relationships.append(relationship)
        return relationships

    def write_bdio(self, output_path=None):
        bdio_data = self.generate_bdio()
        bdio_str = json.dumps(bdio_data, indent=4, sort_keys=True)
        if output_path:
            file_name = "bdio"
            if self.tree.name:
                file_name = self.tree.name
            generate_file(
                bdio_str, file_name, output_path, BDIO_EXTENSION)
        return bdio_str
