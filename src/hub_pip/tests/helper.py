

import os

from hub_pip import __version__
from hub_pip.BlackDuckConfig import BlackDuckConfig
from hub_pip.LogHandler import *


VALID = "valid.ini"
INVALID = "invalid.ini"
BROKEN = "broken.ini"

CLEANUP = True

BASE = "src/hub_pip/tests/resources/"

REQUIREMENTS = BASE + "requirements.txt"
SMALL_BDIO = BASE + "small_bdio.jsonld"
BIG_BDIO = BASE + "big_bdio.jsonld"


def get_config(file_name):
    file_path = BASE + file_name
    config = BlackDuckConfig.from_file(file_path)
    config.project_name = "hub-pip"
    config.project_version_name = __version__
    return config


def cleanup(files_to_remove):
    if CLEANUP:
        if isinstance(files_to_remove, list):
            for file in files_to_remove:
                cleanup(file)
        if os.path.exists(files_to_remove):
            os.remove(files_to_remove)
        else:
            debug(files_to_remove + " does not exist")
            assert(False)


def get_file(file_path):
    file_str = None
    with open(file_path, "r") as file:
        file_str = file.read()
    return file_str
