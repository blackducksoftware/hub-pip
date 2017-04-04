from hub_pip.FileHandler import generate_file, FLAT_EXTENSION, TREE_EXTENSION


class TreeHandler(object):
    tree = None

    def __init__(self, tree):
        self.tree = tree

    def render_tree(self,  output_path=None):
        result = self._render_tree_helper(self.tree)
        if output_path:
            generate_file(
                result, self.tree.name, output_path, TREE_EXTENSION)
        return result

    def _render_tree_helper(self, tree_node, layer=1):
        result = tree_node.name + "==" + tree_node.version
        dependencies = sorted(tree_node.dependencies, key=lambda x: x.name)
        for dependency in dependencies:
            result += "\n" + (" " * 4 * layer)
            result += self._render_tree_helper(dependency, layer + 1)
        return result

    def render_flat(self, output_path=None):
        flat_list = self.tree.flatten()
        result = ""
        flat_list.sort(key=lambda x: x.name)
        for node in flat_list:
            result += node.name + "==" + node.version + "\n"

        if output_path:
            generate_file(
                result, self.tree.name, output_path, FLAT_EXTENSION)
        return result
