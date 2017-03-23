import requests

from hub_python_plugin.BlackDuckSerializer import *
from hub_python_plugin.api.HubServerConfig import HubServerConfig


class RestConnection(object):

    JSPRING = "/j_spring_security_check"

    _session = None
    config = None  # HubServerConfig

    def __init__(self, hub_server_config):
        self._session = requests.session()
        if isinstance(hub_server_config, HubServerConfig):
            self.config = hub_server_config

    def make_get_request(self, path, params=None, headers=None, proxies=None):
        """
        path: str
        queryParameters: dict
        """
        url = self.build_url(path)
        return self.make_get_request_link(url, params=params, headers=headers, proxies=proxies)

    def make_get_request_link(self, url, params=None, headers=None, proxies=None):
        """
        url: str
        queryParameters: dict
        """
        if headers is None:
            headers = self.headers_json()

        response = None
        if params:
            response = self._session.get(
                url, params=params, headers=headers, proxies=proxies)
        else:
            response = self._session.get(url, headers=headers, proxies=proxies)

        return response

    def make_post_request(self, path, content, headers=None, proxies=None):
        """
        path: str
        content: str or dict
        """
        url = self.build_url(path)
        response = self._session.post(url, content, headers=headers, proxies=proxies)
        return response

    def headers_json(self):
        headers = {"content-type": "application/json"}
        return headers

    def headers_jsonld(self):
        headers = {"content-type": "application/ld+json"}
        return headers

    def get_proxies(self):
        proxies = None
        if self.config.hub_proxy_host is not None:
            protocol = self.config.hub_url.split("://")[0]
            user = self.config.hub_proxy_username
            password = self.config.hub_proxy_password
            host = self.config.hub_proxy_host
            port = self.config.hub_proxy_port
            url = None
            if port:
                address = "{}:{}".format(host, port)
            else:
                address = host
            if user and password:
                url = "{}://{}:{}@{}".format(protocol, user, password, address)
            else:
                url = "{}://{}".format(protocol, address)
            proxies = {
                protocol: url
            }
        return proxies

    def build_url(self, path):
        url = "{}/{}".format(self.config.hub_url, path)
        return url

    def check_policy(self):
        pass

    def remap_list(self, data, cls):
        data = [map_to_object(item, cls) for item in data]
        return data

    def remap_object(self, data, cls):
        data = map_to_object(data, cls)
        return data
