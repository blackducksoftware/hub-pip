import distutils
import json
import os
import tempfile

import pip
import pkg_resources
from setuptools.package_index import PackageIndex

from hub_pip.BlackDuckPackage import BlackDuckPackage


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

        return tree

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
