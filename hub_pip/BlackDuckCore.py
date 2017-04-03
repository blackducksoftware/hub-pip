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
        self.project_name = black_duck_config.project_version_name


def get_raw_dependencies(package, raise_on_fail):
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
        if raise_on_fail:
            raise Exception(message + package)
        print(message + package)
    return dependencies


def get_dependencies(pkg, raise_on_fail):
    dependencies = []

    for dependency in pkg.requires():
        pkg = get_best(dependency, raise_on_fail)
        if pkg:
            pkg_dependencies = get_dependencies(pkg, raise_on_fail)
            package = BlackDuckPackage(
                pkg.key, pkg.project_name, pkg.version, pkg_dependencies)
            dependencies.append(package)
    return dependencies


# Can take in an object with a key or just a string
def get_best(dependency, raise_on_fail):
    installed = pip.get_installed_distributions(
        local_only=False, user_only=False)

    if hasattr(dependency, "key"):
        dependency = dependency.key
    elif hasattr(dependency, "name"):
        dependency = dependency.name

    for pkg in installed:
        if pkg.key.lower() == dependency.lower():
            return pkg

    if raise_on_fail == True:
        raise Exception(message + dependency)
    print message + dependency

    return None
