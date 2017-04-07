
"""
hub_pip
Usage:
  hub_pip config [<file_path>]
  hub_pip <project-name> <project-version>
        [
        ((-c | --Config) <hub_config.ini>) 
        --Hub-Url=<huburl>
        --Hub-Username=<username>
        --Hub-Password=<password>
        --Hub-Proxy-Host=<None>
        --Hub-Proxy-Port=<None>
        --Hub-Proxy-Username=<None>
        --Hub-Proxy-Password=<None>
        --Hub-Timeout=<120>
        --Hub-ScanTimeout=<300>
        --Hub-CodeLocationName=<None>
        --OutputDirectory=<build/output/>
        --RequirementsFile=<None>
        --IgnoreFailure=<False>
        --CreateFlatDependencyList=<True>
        --CreateTreeDependencyList=<True>
        --CreateHubBdio=<True>
        --DeployHubBdio=<False>
        --CheckPolicies=<False>
        ]
        
Options:
    -h --help                            Show this screen.
    --version                            Show version.
    
Examples:
  hub-pip -c config.ini --DeployHubBdio=True
Help:
  For help using this tool, please open an issue on the Github_pip repository:
  https://github.com/BlackDuckSoftware/hub-python-plugin
"""


"""
hub_pip [
            ((-c | --Config) <hub_config.ini>) 
            --Hub-Url=<huburl>
            --Hub-Username=<username>
            --Hub-Password=<password>
            --Hub-Proxy-Host=<None>
            --Hub-Proxy-Port=<None>
            --Hub-Proxy-Username=<None>
            --Hub-Proxy-Password=<None>
            --Hub-Timeout=<120>
            --Hub-ScanTimeout=<300>
            --Hub-CodeLocationName=<None>
            --OutputDirectory=<build/output/>
            --RequirementsFile=<None>
            --IgnoreFailure=<False>
            --CreateFlatDependencyList=<True>
            --CreateTreeDependencyList=<True>
            --CreateHubBdio=<True>
            --DeployHubBdio=<False>
            --CheckPolicies=<False>
            ]
"""

from inspect import getmembers, isclass
import os
import shutil
import sys

from docopt import docopt

from hub_pip.BlackDuckConfig import BlackDuckConfig
from hub_pip.BlackDuckCore import BlackDuckCore

from . import __version__ as VERSION


def cli():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=VERSION)

    if options["<project-name>"]:
        options["--Project-Name"] = options["<project-name>"]

    if options["<project-version>"]:
        options["--Project-Version"] = options["<project-version>"]

    if options["config"]:
        if options["<file_path>"]:
            copy_config(path=options["<file_path>"])
        else:
            copy_config()
    else:
        main(options)


def main(options):
    """Build config file from options"""
    config_str = "[Black Duck Config]\n"

    for key, value in options.items():
        if "--" in key and value is not None and value is not "--Config":
            field = key.replace("--", "")
            config_option = field + " = " + str(value) + "\n"
            config_str += config_option

    config = None
    if options["-c"] or options["--Config"]:
        config_file_path = options["<hub_config.ini>"]
        config = BlackDuckConfig.from_file(config_file_path)

    config = BlackDuckConfig.from_string(config_str, black_duck_config=config)

    core = BlackDuckCore(config)
    core.run()


def copy_config(path=None):
    pkgdir = sys.modules["hub_pip"].__path__[0]
    fullpath = os.path.join(pkgdir, "../../sample_config.ini")
    if path:
        shutil.copy(fullpath, path)
    else:
        shutil.copy(fullpath, os.getcwd())
