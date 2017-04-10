import os

from hub_pip.BlackDuckCore import BlackDuckCore
from hub_pip.FileHandler import get_file_path, TREE_EXTENSION
from hub_pip.tests.helper import *
import pip
import six


class TestTreeList:

    def test_tree(self):
        config = get_config(VALID)
        self._test_tree(config, 5)

    def test_tree_with_requirements(self):
        config = get_config(VALID)
        config.requirements_file_path = REQUIREMENTS

        if six.PY2:
            self._test_tree(config, 64)
        else:
            self._test_tree(config, 60)

    def _test_tree(self, config, length):
        config.tree_list = True
        tree_list_name = get_file_path(
            "hub-pip", config.output_path, TREE_EXTENSION)

        core = BlackDuckCore(config)
        core.run()

        assert(os.path.exists(tree_list_name))

        tree_list = get_file(tree_list_name).strip().split("\n")

        assert(len(tree_list) == length)

        cleanup(tree_list_name)
