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

def get_dependencies(pkg):
    dependencies = []
    for dependency in pkg.requires():
        pkg = get_best(dependency)
        if pkg:
            pkg_dependencies = get_dependencies(pkg)
            package = Package.make_package(
                pkg.key, pkg.version, pkg_dependencies)
            dependencies.append(package)
    return dependencies


def get_best(dependency):  # Needs some work to check for multiple packages
    installed = pip.get_installed_distributions(
        local_only=False, user_only=False)

    for pkg in installed:
        if pkg.key == dependency.key:
            return pkg
    print("No match found for: " + dependency.key)
    return None


def render_tree(root, layer=0):
    result = root.name + "==" + root.version
    dependencies = sorted(root.dependencies, key=lambda x: x.name)
    for dependency in dependencies:
        result += "\n" + (" " * 4 * layer)
        result += render_tree(dependency, layer + 1)
    return result

def render_flat(pkgs):
    result = ""
    for pkg in pkgs:
        full_pkg = get_best(pkg)
        result += full_pkg.key + "==" + full_pkg.version + "\n"
    return result


def get_setup_dependencies(package):
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
