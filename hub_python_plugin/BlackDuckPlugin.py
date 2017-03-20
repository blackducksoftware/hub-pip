from setuptools import Command
import argparse
import Package
from BlackDuckCore import *

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

    def run(self):
        """Run command."""

        flat = self.flat_list
        tree = self.tree_list

        project_av = self.distribution.get_name() + "==" + self.distribution.get_version()

        if(tree):
            pkgs = get_setup_dependencies(project_av)
            pkg = pkgs.pop(0)  # The first dependency is itself
            pkg_dependencies = get_dependencies(pkg)
            root = Package.make_package(pkg.key, pkg.version, pkg_dependencies)
            print(render_tree(root, 1))

        if(flat):
            pkgs = get_setup_dependencies(project_av)
            pkg = pkgs.pop(0)  # The first dependency is itself
            pkgs = list(set(pkgs)) # Remove duplicates
            pkgs.sort(key = lambda x: x.key)
            print(render_flat(pkgs))
