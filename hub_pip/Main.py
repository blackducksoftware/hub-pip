
"""
hub-pip
Usage:
  hub-pip 
        <ProjectName>
        <ProjectVersion>
        [
        (-c <hub_config.ini>) 
        --Hub.Url=<huburl>
        --Hub.Username=<username>
        --Hub.Password=<password>
        --Hub.Proxy.Host=<None>
        --Hub.Proxy.Port=<None>
        --Hub.Proxy.Username=<None>
        --Hub.Proxy.Password=<None>
        --Hub.Timeout=<120>
        --Hub.ScanTimeout=<300>
        --Hub.CodeLocationName=<None>
        --OutputDirectory=<build/output/>
        --IgnoreFailure=<False>
        --CreateFlatDependencyList=<True>
        --CreateTreeDependencyList=<True>
        --CreateHubBdio=<True>
        --DeployHubBdio=<True>
        --CheckPolicies=<True>
        ]

Options:
    -h --help                            Show this screen.
    --version                            Show version.
    (-c <hub_config.ini>)                Path to hub configuration file
    --Hub.Url=<huburl>                   The url of the hub
    --Hub.Username=<username>            The username to login to the hub
    --Hub.Password=<password>            The password to login 
    --Hub.Proxy.Host=<None>              The proxy host
    --Hub.Proxy.Port=<None>              
    --Hub.Proxy.Username=<None>
    --Hub.Proxy.Password=<None>
    --Hub.Timeout=<120>
    --Hub.ScanTimeout=<300>
    --Hub.CodeLocationName=<None>
    --OutputDirectory=<build/output/>
    --IgnoreFailure=<False>
    --CreateFlatDependencyList=<True>
    --CreateTreeDependencyList=<True>
    --CreateHubBdio=<True>
    --DeployHubBdio=<True>
    --CheckPolicies=<True>
Examples:
  hub-pip test
Help:
  For help using this tool, please open an issue on the Github_pip repository:
  https://github.com/BlackDuckSoftware/hub-python-plugin
"""


from inspect import getmembers, isclass
from json import dumps

from docopt import docopt
from hub_pip.BlackDuckPlugin import BlackDuckCommand

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import hub_pip.commands

    options = docopt(__doc__, version=VERSION)

    """TODO: Parse options to BlackDuckConfig class"""
