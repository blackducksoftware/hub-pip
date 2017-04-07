
import distutils
import json
import os
import tempfile
import traceback

import pip
import pkg_resources
from setuptools.package_index import PackageIndex

from hub_pip.BlackDuckPackage import BlackDuckPackage
from hub_pip.FileHandler import *
from hub_pip.LogHandler import *
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


class BlackDuckCore(object):

    config = None

    project_name = None
    project_version = None

    fail = False
    fail_on_match = False

    def __init__(self, black_duck_config):
        self.config = black_duck_config
        self.project_name = black_duck_config.project_name
        self.project_version = black_duck_config.project_version_name
        self.fail = not black_duck_config.ignore_failure

    def run(self):
        try:
            return self.execute()
        except Exception as e:
            error(message=e, exit=self.fail)
        return None

    def execute(self):
        info("Gathering dependencies")

        if self.project_name is None or self.project_version is None:
            error(error("Project name or version is not set", exit=self.fail))

        project_av = self.project_name + "==" + self.project_version
        pkgs = get_raw_dependencies(project_av, self.fail_on_match)
        if pkgs == []:
            error(project_av + " does not appear to be installed")

        pkg = pkgs.pop(0)  # The first dependency is itself
        pkg_dependencies = get_dependencies(pkg, self.fail_on_match)
        optional = self._fetch_optional_requirements()
        if optional:
            pkg_dependencies.extend(optional)

        info("Building dependency tree")

        tree = BlackDuckPackage(pkg.key, pkg.project_name,
                                pkg.version, pkg_dependencies)

        tree_handler = TreeHandler(tree)

        if self.config.flat_list:
            tree_handler.render_flat(self.config.output_path)
            info("Generated: Flat list")

        if self.config.tree_list:
            tree_list = tree_handler.render_tree(self.config.output_path)
            info("Generated: Tree list")

        if self.config.create_hub_bdio:
            self.create_bio(tree)

        if self.config.deploy_hub_bdio:
            self.deploy_bdio(tree)

        if self.config.check_policies:
            try:
                self.check_policies(tree)
            except:
                error(message="Failed to check component policies", exit=self.fail)

        return tree

    def create_bio(self, tree):
        bdio = Bdio(tree, self.config.code_location_name)
        bdio_data = bdio.generate_bdio()
        bdio.write_bdio(output_path=self.config.output_path)
        info("Generated: Black Duck I/O")

    def deploy_bdio(self, tree):
        info("Deploying: Black Duck I/O")
        bdio_file_path = self.config.output_path + "/" + tree.name + ".jsonld"
        try:
            assert os.path.exists(bdio_file_path)
            with open(bdio_file_path, "r") as bdio_file:
                bdio_data = bdio_file.read()
            rc = get_authenticated_api(self.config.hub_server_config)
            linked_data_data_service = LinkedDataDataService(rc)
            linked_data_response = linked_data_data_service.upload_bdio(
                bdio_data)
            info("Black Duck I/O successfully deployed to the hub")
        except:
            error(message="Failed to deploy Black Duck I/O to the hub", exit=self.fail)

    def check_policies(self, tree):
        info("Checking component policy status")
        rc = get_authenticated_api(self.config.hub_server_config)
        version_bom_policy_data_service = VersionBomPolicyDataService(rc)
        waiting_data_service = WaitingDataService(rc, self.config)

        info("Waiting for project to be created")
        project_version_view = waiting_data_service.wait_for_project(
            tree.name, tree.version)
        info("Project created")

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
        info(policy_log)

        if policy_status.overall_status == "IN_VIOLATION":
            error(message="The Hub found: " + policy_status.get_in_violation() +
                  " components in violation", exit=self.fail)
        return policy_status

    def _fetch_optional_requirements(self):
        requirements = self.config.requirements_file_path

        # If the user wants to include their requirements.txt file
        if requirements:
            try:
                assert os.path.exists(requirements), (
                    "The requirements file %s does not exist." % requirements)
                requirements = pip.req.parse_requirements(
                    requirements, session=pip.download.PipSession())
            except:
                error(message="Requirements file @ " + requirements +
                      " was not found", exit=self.fail)

        if requirements is None:
            return None

        pkg_dependencies = []
        for req in requirements:
            req_package = get_best(req.req, self.fail)
            if req_package:
                found = False
                for existing in pkg_dependencies:
                    if existing.key.lower() == req_package.key.lower():
                        found = True
                        break
                if not found:
                    req_dependencies = get_dependencies(
                        req_package, self.fail_on_match)
                    key = req_package.key
                    name = req_package.project_name
                    version = req_package.version
                    dependencies = req_dependencies
                    req_package = BlackDuckPackage(
                        key, name, version, dependencies)
                    pkg_dependencies.append(req_package)

        return pkg_dependencies


def get_raw_dependencies(package, fail_on_match):
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
    except Exception as e:
        m = "No matching packages found for declared dependency: "
        error(message=m + package, exit=fail_on_match)
    return dependencies


def get_dependencies(pkg, fail_on_match):
    dependencies = []

    for dependency in pkg.requires():
        pkg = get_best(dependency, fail_on_match)
        if pkg:
            pkg_dependencies = get_dependencies(pkg, fail_on_match)
            package = BlackDuckPackage(
                pkg.key, pkg.project_name, pkg.version, pkg_dependencies)
            dependencies.append(package)
    return dependencies


# Can take in an object with a key or just a string
def get_best(dependency, fail_on_match):
    installed = pip.get_installed_distributions(
        local_only=False, user_only=False)

    if hasattr(dependency, "key"):
        dependency = dependency.key
    elif hasattr(dependency, "name"):
        dependency = dependency.name

    for pkg in installed:
        if pkg.key.lower() == dependency.lower():
            return pkg
    m = "No matching packages found for declared dependency: "
    error(message=m + dependency, exit=fail_on_match)
    return None
