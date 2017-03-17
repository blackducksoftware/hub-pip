from setuptools import Command
import argparse
import pip
import pkg_resources
import distutils
import Package

__version__ = "0.0.1"


class BlackDuckCommand(Command):

    description = "Setuptools hub_python_plugin"

    user_options = [
        ("config-path=", "c", "Path to Black Duck Configuration file"),
        ("flat-list=", "f", "Generate flat list"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.config_path = None
        self.flat_list = False

    def finalize_options(self):
        """Post-process options."""
        if self.config_path:
            assert os.path.exists(self.config_path), (
                "Black Duck Config file %s does not exist." % self.config_path)

    def run(self):
        """Run command."""

        flat = self.flat_list
        project_av = self.distribution.get_name() + "==" + self.distribution.get_version()
        if(flat):
            pkgs = get_raw_dependencies(project_av)
            pkg = pkgs.pop(0)
            pkg_dependencies = get_dependencies(pkg)
            root = Package.make_package(pkg.key, pkg.version, pkg_dependencies)
            print(render_tree(root))


def get_dependencies(pkg):
    dependencies = []
    for dependency in pkg.requires():
        pkg = get_best(dependency)
        if pkg:
            pkg_dependencies = get_dependencies(pkg)
            package = Package.make_package(pkg.key, pkg.version, pkg_dependencies)
            dependencies.append(package)
    return dependencies


def get_best(dependency):
    installed = pip.get_installed_distributions(
        local_only=False, user_only=False)
    for pkg in installed:
        if pkg.key == dependency.key:
            return pkg
    print("No match found for: " + dependency.key)
    return None


def render_tree(root, layer=0):
    result = root.name + "==" + root.version
    for dependency in root.dependencies:
        result += "\n" + (" " * 4 * layer)
        result += render_tree(dependency, layer + 1)
    return result

def get_raw_dependencies(package):
    project_requirement = pkg_resources.Requirement.parse(package)

    environment = pkg_resources.Environment(
        distutils.sysconfig.get_python_lib(),
        platform=None,
        python=None
    )

    dependencies = pkg_resources.working_set.resolve(
        [project_requirement], env=environment
    )

    #dependencies = pkg_resources.working_set.find(project_requirement)
    return dependencies
