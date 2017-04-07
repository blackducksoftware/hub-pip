import os

TREE_EXTENSION = "_tree.txt"
FLAT_EXTENSION = "_flat.txt"
BDIO_EXTENSION = ".jsonld"


def get_file_path(file_name, output_path, extension=None):
    file_path = output_path + "/"
    file_path += file_name
    if extension:
        file_path += extension
    return file_path


def generate_file(data, file_name, output_path, file_extension=None):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_file_path = get_file_path(file_name, output_path, file_extension)
    with open(output_file_path, "w+") as output_file:
        output_file.write(data)
    return output_file_path
