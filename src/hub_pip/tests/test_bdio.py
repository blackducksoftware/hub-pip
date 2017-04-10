import json
import os

from hub_pip.BlackDuckCore import BlackDuckCore
from hub_pip.BlackDuckSerializer import map_to_object
from hub_pip.FileHandler import get_file_path, BDIO_EXTENSION
from hub_pip.bdio.BdioComponent import BdioComponent
from hub_pip.bdio.BdioProject import BdioProject
from hub_pip.bdio.BillOfMaterials import BillOfMaterials
from hub_pip.tests.helper import *


class TestBdio:

    def test_bdio(self):
        config = get_config(VALID)
        self._test_bdio(config, SMALL_BDIO)

    def _test_bdio_with_requirements(self):
        config = get_config(VALID)
        config.requirements_file_path = REQUIREMENTS
        self._test_bdio(config, BIG_BDIO)

    def _test_bdio(self, config, bdio_sample):
        config.create_hub_bdio = True
        bdio_file_name = get_file_path(
            "hub-pip", config.output_path, BDIO_EXTENSION)

        core = BlackDuckCore(config)
        core.run()

        assert(os.path.exists(bdio_file_name))

        actual_bdio = None
        with open(bdio_file_name) as bdio_file:
            actual_bdio = json.load(bdio_file)

        expected_bdio = None
        with open(bdio_sample) as bdio_file:
            expected_bdio = json.load(bdio_file)

        compare_bom(expected_bdio, actual_bdio)
        compare_project(expected_bdio, actual_bdio)
        compare_components(expected_bdio, actual_bdio)

        cleanup(bdio_file_name)


def get_type(bdio, type, cls):
    node = None
    for component in bdio:
        if component["@type"] == type:
            node = map_to_object(component, cls)
            break
    return node


def get_type_list(bdio, type, cls):
    nodes = []
    for component in bdio:
        if component["@type"] == type:
            node = map_to_object(component, cls)
            nodes.append(node)
    return nodes


def compare_bom(expected_bdio, actual_bdio):
    expected_bom = get_type(expected_bdio, "BillOfMaterials", BillOfMaterials)
    actual_bom = get_type(actual_bdio, "BillOfMaterials", BillOfMaterials)
    expected_bom.name = actual_bom.name
    assert(actual_bom == expected_bom)


def compare_project(expected_bdio, actual_bdio):
    expected_project = get_type(expected_bdio, "Project", BdioProject)
    actual_project = get_type(actual_bdio, "Project", BdioProject)
    expected_project.name = actual_project.name
    expected_project.version = actual_project.version
    expected_project.id = actual_project.id
    expected_project.external_id = actual_project.external_id
    assert(actual_project == expected_project)


def compare_components(expected_bdio, actual_bdio):
    expected_components = get_type_list(
        expected_bdio, "Component", BdioComponent)
    actual_components = get_type_list(actual_bdio, "Component", BdioComponent)
    assert len(actual_components) == len(expected_components)
    for expected_component in expected_components:
        assert(expected_component in actual_components)
