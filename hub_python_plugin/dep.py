import pkg_resources
import distutils


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
