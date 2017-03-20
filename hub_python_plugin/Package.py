class Package(object):
    name = ""
    version = ""
    dependencies = []

    def __init__(self, name, version, dependencies):
        self.name = name
        self.version = version
        self.dependencies = dependencies

    def add_dependency(package):
        dependencies.append(package)

    def render_id():
        id = name + "==" + version
        return id


def make_package(name, version, dependencies):
    package = Package(name, version, dependencies)
    return package
