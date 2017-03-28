import distutils
import json
import os

import pip
import pkg_resources

from bdsplugin.BlackDuckPackage import BlackDuckPackage


try:
    import configparser
except:
    from six.moves import configparser


def get_file_path(file_name, output_path, extension=None):
    file_path = output_path + "/"
    file_path += file_name
    if extension:
        file_path += extension
    return file_path


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
            package = BlackDuckPackage(
                pkg.key, pkg.project_name, pkg.version, pkg_dependencies)
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


def render_flat(flat_list):
    result = ""
    flat_list.sort(key=lambda x: x.name)
    for node in flat_list:
        result += node.name + "==" + node.version + "\n"
    return result


def generate_flat_list(tree, output_path=None):
    flat_pkgs = tree.flatten()  # Remove duplicates
    flattened = render_flat(flat_pkgs)
    if output_path:
        _generate_file(flattened, tree.name, output_path, "_flat.txt")
    return flattened


def generate_tree_list(tree, output_path):
    tree_list = render_tree(tree)
    if output_path:
        _generate_file(tree_list, tree.name, output_path, "_tree.txt")
    return tree_list


def generate_bdio(bdio_data, project_name=None, output_path=None):
    bdio_str = json.dumps(bdio_data, indent=4, sort_keys=True)
    if output_path:
        file_name = "bdio"
        if project_name:
            file_name = project_name
        _generate_file(bdio_str, file_name, output_path, ".jsonld")
    return bdio_str


def _generate_file(data, file_name, output_path, file_extension=None):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_file_path = get_file_path(file_name, output_path, file_extension)
    with open(output_file_path, "w+") as output_file:
        output_file.write(data.encode("utf8"))
