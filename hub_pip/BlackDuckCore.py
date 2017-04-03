import distutils
import json
import os
import tempfile
import traceback

import pip
import pkg_resources
from setuptools.package_index import PackageIndex

from hub_pip.BlackDuckPackage import BlackDuckPackage
from hub_pip.TreeHandler import TreeHandler
from hub_pip.api.AuthenticationDataService import AuthenticationDataService, get_authenticated_api
from hub_pip.api.LinkedDataDataService import LinkedDataDataService
from hub_pip.api.ProjectDataService import ProjectDataService
from hub_pip.api.VersionBomPolicyDataService import VersionBomPolicyDataService
from hub_pip.api.WaitingDataService import WaitingDataService
from hub_pip.bdio.Bdio import Bdio


try:
    import configparser
except:
    from six.moves import configparser


message = "No matching packages found for declared dependency: "


class BlackDuckCore(object):

    config = None

    project_name = None
    project_version = None

    def __init__(self, black_duck_config):
        self.config = black_duck_config
        self.project_name = black_duck_config.project_name
        self.project_version = black_duck_config.project_version_name

    def run(self):
        try:
            self.execute()
        except Exception as exception:
            traceback.print_exc()
            if not self.config.ignore_failure:
                raise exception

    def run(self):
        project_av = self.project_name + "==" + self.project_version

        pkgs = get_raw_dependencies(project_av, self.config.ignore_failure)
        if pkgs == []:
            raise Exception(project_av + " does not appear to be installed")

        pkg = pkgs.pop(0)  # The first dependency is itself
        pkg_dependencies = get_dependencies(pkg, self.config.ignore_failure)
        optional = self._fetch_optional_requirements()
        if optional:
            pkg_dependencies.extend(optional)

        tree = BlackDuckPackage(pkg.key, pkg.project_name,
                                pkg.version, pkg_dependencies)

        tree_handler = TreeHandler(tree)

        if self.config.flat_list:
            flattened = tree_handler.render_flat(self.config.output_path)
            # print(flattened)

        if self.config.tree_list:
            tree_list = tree_handler.render_tree(self.config.output_path)
            # print(tree_list)

        if self.config.create_hub_bdio:
            self.create_bio(tree)

        if self.config.deploy_hub_bdio:
            self.deploy_bdio(tree)

        if self.config.check_policies:
            self.check_policies(tree)

        return tree

    def create_bio(self, tree):
        print("Generating Black Duck I/O")
        bdio = Bdio(tree, self.config.code_location_name)
        bdio_data = bdio.generate_bdio()
        bdio.write_bdio(output_path=self.config.output_path)
        print("Successfully generated Black Duck I/O")

    def deploy_bdio(self, tree):
        print("Deploying Black Duck I/O")
        bdio_file_path = self.config.output_path + "/" + tree.name + ".jsonld"
        assert os.path.exists(bdio_file_path)
        with open(bdio_file_path, "r") as bdio_file:
            bdio_data = bdio_file.read()
        rc = get_authenticated_api(self.config.hub_server_config)
        linked_data_data_service = LinkedDataDataService(rc)
        linked_data_response = linked_data_data_service.upload_bdio(bdio_data)
        print("Black Duck I/O successfully deployed to the hub")

    def check_policies(self, tree):
        rc = get_authenticated_api(self.config.hub_server_config)
        version_bom_policy_data_service = VersionBomPolicyDataService(rc)
        waiting_data_service = WaitingDataService(rc, self.config)

        print("Waiting for project to be created")
        project_version_view = waiting_data_service.wait_for_project(
            tree.name, tree.version)
        print("Project created")

        waiting_data_service.wait_for_scan(project_version_view)
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

    def _fetch_optional_requirements(self):
        requirements = self.config.requirements_file_path
        ignore_failure = self.config.ignore_failure

        # If the user wants to include their requirements.txt file
        if requirements:
            assert os.path.exists(requirements), (
                "The requirements file %s does not exist." % requirements)
            requirements = pip.req.parse_requirements(
                requirements, session=pip.download.PipSession())

        if requirements is None:
            return None

        pkg_dependencies = []
        for req in requirements:
            req_package = get_best(req.req, ignore_failure)
            if req_package:
                found = False
                for existing in pkg_dependencies:
                    if existing.key.lower() == req_package.key.lower():
                        found = True
                        break
                if not found:
                    req_dependencies = get_dependencies(
                        req_package, ignore_failure)
                    key = req_package.key
                    name = req_package.project_name
                    version = req_package.version
                    dependencies = req_dependencies
                    req_package = BlackDuckPackage(
                        key, name, version, dependencies)
                    pkg_dependencies.append(req_package)

        return pkg_dependencies


def get_raw_dependencies(package, ignore_failure):
    dependencies = []
    try:
        project_requirement = pkg_resources.Requirement.parse(package)

        environment = pkg_resources.Environment(
            distutils.sysconfig.get_python_lib(),
            platform=None,
            python=None
        )

        dependencies = pkg_resources.working_set.resolve(
            [project_requirement], env=environment)
    except Exception:
        if ignore_failure == False:
            raise Exception(message + package)
        print(message + package)
    return dependencies


def get_dependencies(pkg, ignore_failure):
    dependencies = []

    for dependency in pkg.requires():
        pkg = get_best(dependency, ignore_failure)
        if pkg:
            pkg_dependencies = get_dependencies(pkg, ignore_failure)
            package = BlackDuckPackage(
                pkg.key, pkg.project_name, pkg.version, pkg_dependencies)
            dependencies.append(package)
    return dependencies


# Can take in an object with a key or just a string
def get_best(dependency, ignore_failure):
    installed = pip.get_installed_distributions(
        local_only=False, user_only=False)

    if hasattr(dependency, "key"):
        dependency = dependency.key
    elif hasattr(dependency, "name"):
        dependency = dependency.name

    for pkg in installed:
        if pkg.key.lower() == dependency.lower():
            return pkg

    if ignore_failure == False:
        raise Exception(message + dependency)
    print message + dependency

    return None
