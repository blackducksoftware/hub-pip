import ConfigParser
from api.HubServerConfig import HubServerConfig


class BlackDuckConfig(object):

    hub_server_config = None
    code_location_name = None

    output_path = "build/output"

    ignore_failure = False
    flat_list = False
    tree_list = False
    create_hub_bdio = False
    deploy_hub_bdio = False
    check_policies = False

    def __init__(self):
        self.hub_server_config = HubServerConfig()

    @classmethod
    def from_nothing(self):
        return BlackDuckConfig()

    @classmethod
    def from_file(self, config_file_path):
        bd_config = BlackDuckConfig()

        config = ConfigParser.RawConfigParser()
        config.allow_no_value = True
        config.read(config_file_path)

        bd_config.hub_server_config = HubServerConfig()

        bd_config.hub_server_config.hub_url = config.get("Hub Connection", "Hub.Url")
        bd_config.hub_server_config.hub_username = config.get("Hub Connection", "Hub.Username")
        bd_config.hub_server_config.hub_password = config.get("Hub Connection", "Hub.Password")

        bd_config.hub_server_config.hub_proxy_host = config.get("Hub Connection", "Hub.Proxy.Host")
        bd_config.hub_server_config.hub_proxy_port = config.get("Hub Connection", "Hub.Proxy.Port")
        bd_config.hub_server_config.hub_proxy_username = config.get("Hub Connection", "Hub.Proxy.Username")
        bd_config.hub_server_config.hub_proxy_password = config.get("Hub Connection", "Hub.Proxy.Password")

        bd_config.hub_server_config.hub_timeout = config.get("Hub Connection", "Hub.Timeout")
        bd_config.hub_server_config.hub_scan_timeout = config.get("Hub Connection", "Hub.ScanTimeout")

        bd_config.code_location_name = config.get("Hub Connection", "Hub.CodeLocationName")

        bd_config.output_path = config.get("Paths", "OutputDirectory")

        bd_config.ignore_failure = config.getboolean("Options", "IgnoreFailure")
        bd_config.flat_list = config.getboolean("Options", "CreateFlatDependencyList")
        bd_config.tree_list = config.getboolean("Options", "CreateTreeDependencyList")
        bd_config.create_hub_bdio = config.getboolean("Options", "CreateHubBdio")
        bd_config.deploy_hub_bdio = config.getboolean("Options", "DeployHubBdio")
        bd_config.check_policies = config.getboolean("Options", "CheckPolicies")

        bd_config.verify()
        return bd_config

    def verify(self):
        for k, v in self.__dict__.items():
            if v == "None":
                self.__dict__[k] = None
