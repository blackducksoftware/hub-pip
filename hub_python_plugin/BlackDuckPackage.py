from bdio.BdioExternalIdentifier import BdioExternalIdentifier


class BlackDuckPackage(object):

    key = None
    name = None
    version = None
    dependencies = []

    def __init__(self, key, name, version, dependencies):
        self.key = key
        self.name = name
        self.version = version
        self.dependencies = dependencies

    def add_dependency(self, package):
        self.dependencies.append(package)

    def render_id(self):
        id_ = self.name + "==" + self.version
        return id_

    def get_internal_id(self):
        return "data:" + self.name + "/" + self.version

    def get_external_id(self):
        external_id = BdioExternalIdentifier()
        external_id.forge = "pypi"
        external_id.external_identifier = self.name + "/" + self.version
        return external_id

    def flatten(self):
        flattened = []
        for pkg in self.dependencies:
            pkg_id = pkg.render_id()
            found = False
            for flattened_pkg in flattened:
                if flattened_pkg.render_id() == pkg_id:
                    found = True
                    break
            if not found:
                flattened.append(pkg)
                flattened.extend(pkg.flatten())
        return flattened

def make_package(key, name, version, dependencies):
    package = BlackDuckPackage(key, name, version, dependencies)
    return package
