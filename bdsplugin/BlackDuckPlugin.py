import traceback

import pip
from setuptools import Command

from bdsplugin.BlackDuckConfig import BlackDuckConfig
from bdsplugin.BlackDuckCore import *
import bdsplugin.BlackDuckPackage
from bdsplugin.api.AuthenticationDataService import AuthenticationDataService
from bdsplugin.api.LinkedDataDataService import LinkedDataDataService
from bdsplugin.api.ProjectDataService import ProjectDataService
from bdsplugin.api.RestConnection import RestConnection
from bdsplugin.api.VersionBomPolicyDataService import VersionBomPolicyDataService
from bdsplugin.api.WaitingDataService import WaitingDataService
from bdsplugin.bdio.Bdio import Bdio


__version__ = "0.0.1"


class BlackDuckCommand(Command):

    description = "Setuptools bdsplugin"

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
            self.config = BlackDuckConfig.from_file(self.config_path)
        else:
            self.config = BlackDuckConfig.from_nothing()

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
        try:
            self.execute()
        except Exception as exception:
            traceback.print_exc()
            if not self.config.ignore_failure:
                raise Exception("bdsplugin failed to execute to completion")

    def execute(self):
        """Run command."""

        # The user's project's artifact and version
        project_name = self.distribution.get_name()
        project_version = self.distribution.get_version()
        project_av = project_name + "==" + project_version

        pkgs = get_raw_dependencies(project_av)
        pkg = pkgs.pop(0)  # The first dependency is itself
        pkg_dependencies = get_dependencies(pkg)

        if self.file_requirements:
            for req in self.file_requirements:  # req is the project_av
                pkgs.extend(get_raw_dependencies(req))
                best_match = get_best(req)  # Returns a pip dependency object
                other_requirements = get_dependencies(
                    best_match)  # Array of Packages
                new_package = BlackDuckPackage(
                    best_match.key, best_match.project_name, best_match.version, other_requirements)
                pkg_dependencies.append(new_package)  # Add found dependencies

        tree = BlackDuckPackage(pkg.key, pkg.project_name,
                                pkg.version, pkg_dependencies)

        if self.config.flat_list:
            flattened = generate_flat_list(tree, self.config.output_path)
            print(flattened)

        if self.config.tree_list:
            tree_list = generate_tree_list(tree, self.config.output_path)
            print(tree_list)

        if self.config.create_hub_bdio:
            print("Generating Black Duck I/O")
            bdio = Bdio(tree, self.config.code_location_name)
            bdio_data = bdio.generate_bdio()
            bdio_str = generate_bdio(
                bdio_data, project_name=tree.name, output_path=self.config.output_path)
            print("Successfully generated Black Duck I/O")

        if self.config.deploy_hub_bdio:
            print("Deploying Black Duck I/O")
            bdio_file_path = self.config.output_path + "/" + tree.name + ".jsonld"
            assert os.path.exists(bdio_file_path)
            bdio_data = open(bdio_file_path, "r").read()

            rc = self.get_authenticated_api()
            linked_data_data_service = LinkedDataDataService(rc)

            linked_data_response = linked_data_data_service.upload_bdio(
                bdio_data)
            print("Black Duck I/O successfully deployed to the hub")

        if self.config.check_policies:
            rc = self.get_authenticated_api()
            version_bom_policy_data_service = VersionBomPolicyDataService(rc)
            waiting_data_service = WaitingDataService(rc, self.config)

            print("Waiting for project to be created")
            project_version_view = waiting_data_service.wait_for_project(
                tree.name, tree.version)
            print("Project created")

            waiting_data_service.wait_for_scan(
                project_version_view)
            policy_status = version_bom_policy_data_service.get_version_bom_policy_view(
                project_version_view)

            string_builder = []
            string_builder.append("The Hub found: ")
            string_builder.append(policy_status.get_in_violation())
            string_builder.append(" components in violation, ")
            string_builder.append(
                policy_status.get_in_violation_but_overridden())
            string_builder.append(
                " components in violation, but overridden, and ")
            string_builder.append(policy_status.get_not_in_violation())
            string_builder.append(" components not in violation.")
            policy_log = "".join(string_builder)
            print(policy_log)

            if policy_status.overall_status == "IN_VIOLATION":
                raise Exception(
                    "The Hub found: " + policy_status.get_in_violation() + " components in violation")

    def get_authenticated_api(self):
        rc = RestConnection(self.config.hub_server_config)
        authentication_data_service = AuthenticationDataService(rc)
        authentication_response = authentication_data_service.authenticate()
        authentication_response.raise_for_status()
        return rc


def string_to_boolean(string):
    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        raise ValueError
