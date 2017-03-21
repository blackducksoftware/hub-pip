class Package(object):

    key = None
    name = None
    version = None
    dependencies = []

    def __init__(self, key, name, version, dependencies):
        self.key = key
        self.name = name
        self.version = version
        self.dependencies = dependencies

    def add_dependency(package):
        dependencies.append(package)

    def render_id():
        id = name + "==" + version
        return id


def make_package(key, name, version, dependencies):
    package = Package(key, name, version, dependencies)
    return package
