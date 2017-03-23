import json
import os

import pip
from setuptools import Command

import BlackDuckPackage
from api.HubApi import HubApi
from bdio.Bdio import Bdio
from BlackDuckConfig import BlackDuckConfig as Config
from BlackDuckCore import *

__version__ = "0.0.1"


class BlackDuckCommand(Command):

    description = "Setuptools hub_python_plugin"

    user_options = [
        ("config-path=", "c", "Path to Black Duck Configuration file"),
        ("requirements-path=", "r", "Path to your requirements.txt file"),
        ("flat-list=", "f", "Generate flat list"),
        ("tree-list=", "t", "Generate tree list"),
        ("hub-url=", "h", "The url to use for bdio deployment"),
        ("hub-username=", "u", "The username to use for bdio deployment"),
        ("hub-password=", "p", "The password to use for bdio deployment"),
    ]

    config = None

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.config_path = None
        self.requirements_path = None
        self.flat_list = None
        self.tree_list = None
        self.file_requirements = None
        self.hub_url = None
        self.hub_username = None
        self.hub_password = None

    def finalize_options(self):
        """Post-process options."""
        # If the user wants to use a config file. Necessary for hub connection
        provided_config = self.config_path is not None
        if provided_config:
            assert os.path.exists(self.config_path), (
                "Black Duck Config file %s does not exist." % self.config_path)
            self.config = Config.from_file(self.config_path)
        else:
            self.config = Config.from_nothing

        if self.flat_list is not None:
            self.config.flat_list = string_to_boolean(self.flat_list)

        if self.tree_list is not None:
            self.config.tree_list = string_to_boolean(self.tree_list)

        if self.hub_url is not None:
            self.config.hub_server_config.hub_url = self.hub_url

        if self.hub_username is not None:
            self.config.hub_server_config.hub_username = self.hub_username

        if self.hub_password is not None:
            self.config.hub_server_config.hub_password = self.hub_password

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

        if self.file_requirements:
            for req in self.file_requirements:  # req is the project_av
                pkgs.extend(get_raw_dependencies(req))
                best_match = get_best(req)  # Returns a pip dependency object
                other_requirements = get_dependencies(
                    best_match)  # Array of Packages
                new_package = BlackDuckPackage.make_package(
                    best_match.key, best_match.project_name, best_match.version, other_requirements)
                pkg_dependencies.append(new_package)  # Add found dependencies

        if self.config.flat_list:
            flat_pkgs = list(set(pkgs))  # Remove duplicates
            print(render_flat(flat_pkgs))

        tree = BlackDuckPackage.make_package(
            pkg.key, pkg.project_name, pkg.version, pkg_dependencies)

        if self.config.tree_list:
            print(render_tree(tree))

        if self.config.create_hub_bdio:
            print(self.config.code_location_name)
            bdio = Bdio(tree, self.config.code_location_name)
            bdio_data = bdio.generate_bdio()
            path = self.config.output_path
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + "/bdio.jsonld", "w+") as bdio_file:
                json.dump(bdio_data, bdio_file, ensure_ascii=False, indent=4, sort_keys=True)

        if self.config.deploy_hub_bdio:
            bdio_file_path = self.config.output_path + "/bdio.jsonld"
            assert os.path.exists(bdio_file_path)
            bdio_file = open(bdio_file_path, "r")
            bdio_data = bdio_file.read()

            api = HubApi(self.config.hub_server_config)
            api.authenticate()
            response = api.upload_bdio(bdio_data)
            response.raise_for_status()


def string_to_boolean(string):
    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        raise ValueError
