import Config
import os

import pip
from setuptools import Command

import Package
from BlackDuckCore import *

__version__ = "0.0.1"


class BlackDuckCommand(Command):

    description = "Setuptools hub_python_plugin"

    user_options = [
        ("config-path=", "c", "Path to Black Duck Configuration file"),
        ("requirements-path=", "r", "Path to your requirements.txt file"),
        ("flat-list=", "f", "Generate flat list"),
        ("tree-list=", "t", "Generate tree list"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.config_path = None
        self.requirements_path = None
        self.flat_list = False
        self.tree_list = False
        self.file_requirements = None

    def finalize_options(self):
        """Post-process options."""
        # If the user wants to use a config file. Necessary for hub connection
        if self.config_path:
            assert os.path.exists(self.config_path), (
                "Black Duck Config file %s does not exist." % self.config_path)
            config = Config.make_config()
            config.load_config(self.config_path)

            self.config = config
            self.flat_list = config.flat_list
            self.tree_list = config.tree_list

        # If the user wants to include their requirements.txt file
        if self.requirements_path:
            assert os.path.exists(self.requirements_path), (
                "The requirements file %s does not exist." % self.requirements_path)
            file_requirements = pip.req.parse_requirements(
                self.requirements_path, session=pip.download.PipSession())
            self.file_requirements = [r.req.name for r in file_requirements]

    def run(self):
        """Run command."""

        # The user's project's artifact and version
        project_av = self.distribution.get_name() + "==" + self.distribution.get_version()

        pkgs = get_raw_dependencies(project_av)
        pkg = pkgs.pop(0)  # The first dependency is itself
        pkg_dependencies = get_dependencies(pkg)

        if(self.file_requirements):
            for req in self.file_requirements:  # req is the project_av
                pkgs.extend(get_raw_dependencies(req))
                best_match = get_best(req)  # Returns a pip dependency object
                other_requirements = get_dependencies(best_match)  # Array of Packages
                new_package = Package.make_package(
                    best_match.key, best_match.version, other_requirements)
                pkg_dependencies.append(new_package)  # Add found dependencies

        if(self.flat_list):
            flat_pkgs = list(set(pkgs))  # Remove duplicates
            print(render_flat(flat_pkgs))

        if(self.tree_list):
            root = Package.make_package(pkg.key, pkg.version, pkg_dependencies)
            print(render_tree(root))
