from setuptools import Command
import argparse
import Package
from BlackDuckCore import *
import Config
import os

__version__ = "0.0.1"


class BlackDuckCommand(Command):

    description = "Setuptools hub_python_plugin"

    user_options = [
        ("config-path=", "c", "Path to Black Duck Configuration file"),
        ("flat-list=", "f", "Generate flat list"),
        ("tree-list=", "t", "Generate tree list"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.config_path = None
        self.flat_list = False
        self.tree_list = False

    def finalize_options(self):
        """Post-process options."""
        if self.config_path:
            assert os.path.exists(self.config_path), (
                "Black Duck Config file %s does not exist." % self.config_path)
            config = Config.make_config()
            config.load_config(self.config_path)

            self.config = config

            self.flat_list = config.flat_list
            self.tree_list = config.tree_list

    def run(self):
        """Run command."""

        project_av = self.distribution.get_name() + "==" + self.distribution.get_version()

        pkgs = get_setup_dependencies(project_av)
        pkg = pkgs.pop(0)  # The first dependency is itself

        if(self.flat_list):
            flat_pkgs = list(set(pkgs)) # Remove duplicates
            print(render_flat(flat_pkgs))

        if(self.tree_list):
            pkg_dependencies = get_dependencies(pkg)
            root = Package.make_package(pkg.key, pkg.version, pkg_dependencies)
            print(render_tree(root))
