try:
    import configparser
except:
    from six.moves import configparser
import distutils

import pip
import pkg_resources

from bdsplugin.BlackDuckPackage import BlackDuckPackage


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


def get_dependencies(pkg):
    dependencies = []
    for dependency in pkg.requires():
        pkg = get_best(dependency)
        if pkg:
            pkg_dependencies = get_dependencies(pkg)
            package = BlackDuckPackage(pkg.key, pkg.project_name, pkg.version, pkg_dependencies)
            dependencies.append(package)
    return dependencies


def get_best(dependency):  # Can take in an object with a key or just a string
    installed = pip.get_installed_distributions(
        local_only=False, user_only=False)

    if hasattr(dependency, "key"):
        dependency = dependency.key

    for pkg in installed:
        if pkg.key == dependency:
            return pkg
    print("No match found for: " + dependency)
    return None


def render_tree(root, layer=1):
    result = root.name + "==" + root.version
    dependencies = sorted(root.dependencies, key=lambda x: x.name)
    for dependency in dependencies:
        result += "\n" + (" " * 4 * layer)
        result += render_tree(dependency, layer + 1)
    return result


def render_flat(pkgs):
    result = ""
    pkgs.sort(key=lambda x: x.key)
    for pkg in pkgs:
        full_pkg = get_best(pkg)
        result += full_pkg.key + "==" + full_pkg.version + "\n"
    return result
