import ConfigParser


class Config(object):

    hub_url = None
    hub_username = None
    HubPassword = None

    hub_proxy_host = None
    hub_proxy_port = None
    hub_proxy_username = None
    hub_proxy_password = None

    hub_timeout = 120
    hub_scan_timeout = 300

    output_path = "build/output"

    ignore_failure = False
    flat_list = False
    tree_list = False
    create_hub_bdio = True
    deploy_hub_bdio = True
    create_hub_report = True
    check_policies = True

    def __init__(self):
        pass

    def load_config(self, config_file_path):
        config = ConfigParser.RawConfigParser()
        config.read(config_file_path)

        self.hub_url = config.get("Hub Connection", "Hub.Url")

        self.flat_list = config.getboolean(
            "Options", "CreateFlatDependencyList")
        self.tree_list = config.getboolean(
            "Options", "CreateTreeDependencyList")


def make_config():
    config = Config()
    return config
