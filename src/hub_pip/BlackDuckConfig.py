from io import StringIO

import six

from hub_pip.api.HubServerConfig import HubServerConfig


try:
    import configparser
except:
    from six.moves import configparser


class BlackDuckConfig(object):

    project_name = None
    project_version_name = None

    hub_server_config = None
    code_location_name = None

    output_path = "build/blackduck"
    requirements_file_path = None

    ignore_failure = True
    flat_list = False
    tree_list = False
    create_hub_bdio = True
    deploy_hub_bdio = False
    check_policies = False

    section_name = "Black Duck Config"

    def __init__(self):
        self.hub_server_config = HubServerConfig()

    @classmethod
    def from_nothing(self):
        return BlackDuckConfig()

    @classmethod
    def from_file(self, config_file_path):
        config_str = None
        with open(config_file_path, "r") as config_file:
            config_str = config_file.read()
        return self.from_string(config_str)

    @classmethod
    def from_string(self, config_str, black_duck_config=None):
        bd_config = black_duck_config
        if bd_config is None:
            bd_config = self.from_nothing()

        string_buffer = None
        if six.PY2:
            string_buffer = StringIO(unicode(config_str))
        else:
            string_buffer = StringIO(config_str)

        config = configparser.RawConfigParser()
        config.allow_no_value = True
        config.readfp(string_buffer)

        """Initialize defaults"""
        url = bd_config.hub_server_config.hub_url
        username = bd_config.hub_server_config.hub_username
        password = bd_config.hub_server_config.hub_password
        p_host = bd_config.hub_server_config.hub_proxy_host
        p_port = bd_config.hub_server_config.hub_proxy_port
        p_username = bd_config.hub_server_config.hub_proxy_username
        p_password = bd_config.hub_server_config.hub_proxy_password
        timeout = bd_config.hub_server_config.hub_timeout
        s_timeout = bd_config.hub_server_config.hub_scan_timeout

        code_loc = bd_config.code_location_name
        output_path = bd_config.output_path
        requirements = bd_config.requirements_file_path

        i_fail = bd_config.ignore_failure
        flat = bd_config.flat_list
        tree = bd_config.tree_list
        bdio = bd_config.create_hub_bdio
        deploy = bd_config.deploy_hub_bdio
        policies = bd_config.check_policies

        project = bd_config.project_name
        version = bd_config.project_version_name

        """Parse config string"""
        url = bd_config.get(config, url, "Hub-Url")

        username = bd_config.get(config, username, "Hub-Username")
        password = bd_config.get(config, password, "Hub-Password")
        p_host = bd_config.get(config, p_host, "Hub-Proxy-Host")
        p_port = bd_config.get(config, p_port, "Hub-Proxy-Port")
        p_username = bd_config.get(config, p_username, "Hub-Proxy-Username")
        p_password = bd_config.get(config, p_password, "Hub-Proxy-Password")
        timeout = bd_config.getfloat(config, timeout, "Hub-Timeout")
        s_timeout = bd_config.getfloat(config, s_timeout, "Hub-ScanTimeout")

        code_loc = bd_config.get(config, code_loc, "Hub-CodeLocationName")
        output_path = bd_config.get(config, output_path, "OutputDirectory")
        requirements = bd_config.get(config, requirements, "RequirementsFile")

        i_fail = bd_config.getboolean(config, i_fail, "IgnoreFailure")
        flat = bd_config.getboolean(config, flat, "CreateFlatDependencyList")
        tree = bd_config.getboolean(config, tree, "CreateTreeDependencyList")
        bdio = bd_config.getboolean(config, bdio, "CreateHubBdio")
        deploy = bd_config.getboolean(config, deploy, "DeployHubBdio")
        policies = bd_config.getboolean(config, policies, "CheckPolicies")

        project = bd_config.get(config, project, "Project-Name")
        version = bd_config.get(config, version, "Project-Version")

        bd_config.hub_server_config.hub_url = url
        bd_config.hub_server_config.hub_username = username
        bd_config.hub_server_config.hub_password = password
        bd_config.hub_server_config.hub_proxy_host = p_host
        bd_config.hub_server_config.hub_proxy_port = p_port
        bd_config.hub_server_config.hub_proxy_username = p_username
        bd_config.hub_server_config.hub_proxy_password = p_password
        bd_config.hub_server_config.hub_timeout = timeout
        bd_config.hub_server_config.hub_scan_timeout = s_timeout

        bd_config.code_location_name = code_loc
        bd_config.output_path = output_path
        bd_config.requirements_file_path = requirements

        bd_config.ignore_failure = i_fail
        bd_config.flat_list = flat
        bd_config.tree_list = tree
        bd_config.create_hub_bdio = bdio
        bd_config.deploy_hub_bdio = deploy
        bd_config.check_policies = policies

        bd_config.project_name = project
        bd_config.project_version_name = version

        verify(bd_config)
        verify(bd_config.hub_server_config)

        return bd_config

    def get(self, config, default, property_name):
        value = None
        try:
            value = config.get(self.section_name, property_name)
        except configparser.NoOptionError:
            value = default
        return value

    def getboolean(self, config, default, property_name):
        value = None
        try:
            value = config.getboolean(self.section_name, property_name)
        except configparser.NoOptionError:
            value = default
        return value

    def getfloat(self, config, default, property_name):
        value = None
        try:
            value = config.getfloat(self.section_name, property_name)
        except configparser.NoOptionError:
            value = default
        return value


def verify(obj):
    if obj:
        for k, v in obj.__dict__.items():
            if v == "None":
                obj.__dict__[k] = None
