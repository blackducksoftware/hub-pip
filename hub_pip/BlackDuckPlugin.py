
import os

from setuptools import Command

from hub_pip.BlackDuckConfig import BlackDuckConfig
from hub_pip.BlackDuckCore import BlackDuckCore


__version__ = "0.0.1"


class BlackDuckCommand(Command):

    description = "Setuptools hub_pip"

    user_options = [
        ("config-path=", "c", "Path to Black Duck Configuration file"),
        ("requirements-path=", "r", "Path to your requirements.txt file"),
        ("flat-list=", "f", "True to generate flat list"),
        ("tree-list=", "t", "True to Generate tree list"),
        ("hub-url=", "h", "The url to use for bdio deployment"),
        ("hub-username=", "u", "The username to use for bdio deployment"),
        ("hub-password=", "p", "The password to use for bdio deployment"),
        ("raise-on-matching-fail=", "m",
         "True to raise exception when finding a declared package fails"),
    ]

    config = None
    raise_on_matching_fail = None

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.config_path = None
        self.requirements_path = None
        self.flat_list = None
        self.tree_list = None
        self.hub_url = None
        self.hub_username = None
        self.hub_password = None
        self.raise_on_matching_fail = False

    def finalize_options(self):
        """Post-process options."""
        # If the user wants to use a config file. Necessary for hub connection
        provided_config = self.config_path is not None
        if provided_config:
            assert os.path.exists(self.config_path), (
                "Black Duck Config file %s does not exist." % self.config_path)
            self.config = BlackDuckConfig.from_file(self.config_path)
        else:
            self.config = BlackDuckConfig.from_nothing()

        if self.flat_list is not None:
            self.config.flat_list = string_to_boolean(self.flat_list)

        if self.tree_list is not None:
            self.config.tree_list = string_to_boolean(self.tree_list)

        if self.raise_on_matching_fail is not None:
            self.raise_on_matching_fail = string_to_boolean(
                self.raise_on_matching_fail)

        if self.hub_url is not None:
            self.config.hub_server_config.hub_url = self.hub_url

        if self.hub_username is not None:

            self.config.hub_server_config.hub_username = self.hub_username

        if self.hub_password is not None:
            self.config.hub_server_config.hub_password = self.hub_password

        if self.requirements_path:
            self.config.requirements_file_path = self.requirements_path

    def run(self):
        """Run command."""

        raise_on_fail = self.raise_on_matching_fail

        # The user's project's artifact and version
        project_name = self.distribution.get_name()
        project_version = self.distribution.get_version()

        self.config.project_name = project_name
        self.config.project_version_name = project_version

        core = BlackDuckCore(self.config)
        tree = core.run()


def string_to_boolean(string):
    if string == True:
        return True
    if string == False:
        return False
    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        raise ValueError
