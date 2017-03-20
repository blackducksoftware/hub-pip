import pip
import pkg_resources
import distutils
import Package
import ConfigParser

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


def render_tree(root, layer=1):
    result = root.name + "==" + root.version
    dependencies = sorted(root.dependencies, key=lambda x: x.name)
    for dependency in dependencies:
        result += "\n" + (" " * 4 * layer)
        result += render_tree(dependency, layer + 1)
    return result

def render_flat(pkgs):
    result = ""
    pkgs.sort(key = lambda x: x.key)
    for pkg in pkgs:
        full_pkg = get_best(pkg)
        result += full_pkg.key + "==" + full_pkg.version + "\n"
    return result
