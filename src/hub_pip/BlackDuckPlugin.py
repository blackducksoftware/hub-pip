
import os

from setuptools import Command

from docopt import docopt
from hub_pip.BlackDuckConfig import BlackDuckConfig
from hub_pip.BlackDuckCore import BlackDuckCore
from hub_pip.Main import main

from . import __version__ as VERSION


class BlackDuckCommand(Command):

    description = "Setuptools hub_pip"

    user_options = [
        ("Config=", "c", "Path to Black Duck Configuration file"),
        ("Hub-Url=", None, None),
        ("Hub-Username=", None, None),
        ("Hub-Password=", None, None),
        ("Hub-Proxy-Host=", None, None),
        ("Hub-Proxy-Port=", None, None),
        ("Hub-Proxy-Username=", None, None),
        ("Hub-Proxy-Password=", None, None),
        ("Hub-Timeout=", None, None),
        ("Hub-ScanTimeout=", None, None),
        ("Hub-CodeLocationName=", None, None),
        ("OutputDirectory=", None, None),
        ("RequirementsFile=", None, None),
        ("IgnoreFailure=", None, None),
        ("CreateFlatDependencyList=", None, None),
        ("CreateTreeDependencyList=", None, None),
        ("CreateHubBdio=", None, None),
        ("DeployHubBdio=", None, None),
        ("CheckPolicies=", None, None),
        ("Project-Name=", None, None),
        ("Project-Version=", None, None),
    ]

    options = None

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.Config = None
        self.Hub_Url = None
        self.Hub_Username = None
        self.Hub_Password = None
        self.Hub_Proxy_Host = None
        self.Hub_Proxy_Port = None
        self.Hub_Proxy_Username = None
        self.Hub_Proxy_Password = None
        self.Hub_Timeout = None
        self.Hub_ScanTimeout = None
        self.Hub_CodeLocationName = None
        self.OutputDirectory = None
        self.RequirementsFile = None
        self.IgnoreFailure = None
        self.CreateFlatDependencyList = None
        self.CreateTreeDependencyList = None
        self.CreateHubBdio = None
        self.DeployHubBdio = None
        self.CheckPolicies = None
        self.Project_Name = None
        self.Project_Version = None

    def finalize_options(self):
        if self.Project_Name is None:
            self.Project_Name = self.distribution.get_name()
        if self.Project_Version is None:
            self.Project_Version = self.distribution.get_version()

        self.options = {
            '-c': self.Config,
            '--Config': self.Config,
            '--Hub-Url': self.Hub_Url,
            '--Hub-Username': self.Hub_Username,
            '--Hub-Password': self.Hub_Password,
            '--Hub-Proxy-Host': self.Hub_Proxy_Host,
            '--Hub-Proxy-Port': self.Hub_Proxy_Port,
            '--Hub-Proxy-Username': self.Hub_Proxy_Username,
            '--Hub-Proxy-Password': self.Hub_Proxy_Password,
            '--Hub-Timeout': self.Hub_Timeout,
            '--Hub-ScanTimeout': self.Hub_ScanTimeout,
            '--Hub-CodeLocationName': self.Hub_CodeLocationName,
            '--OutputDirectory': self.OutputDirectory,
            '--RequirementsFile': self.RequirementsFile,
            '--IgnoreFailure': self.IgnoreFailure,
            '--CreateFlatDependencyList': self.CreateFlatDependencyList,
            '--CreateTreeDependencyList': self.CreateTreeDependencyList,
            '--CreateHubBdio': self.CreateHubBdio,
            '--DeployHubBdio': self.DeployHubBdio,
            '--CheckPolicies': self.CheckPolicies,
            '<hub_config.ini>': self.Config,
            '--Project-Name': self.Project_Name,
            '--Project-Version': self.Project_Version,
        }

    def run(self):
        """Run command."""
        main(self.options)


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
