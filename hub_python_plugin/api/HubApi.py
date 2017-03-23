import requests

from HubServerConfig import HubServerConfig

class HubApi(object):

    JSPRING = "/j_spring_security_check"

    _session = None
    config = None  # HubServerConfig

    def __init__(self, hub_server_config):
        self._session = requests.session()
        if isinstance(hub_server_config, HubServerConfig):
            self.config = hub_server_config

    def make_get_request(self, path, queryParameters=None, headers=None, proxies=None):
        """
        path: str
        queryParameters: dict
        """
        url = self.build_url(path)
        response = None
        if(queryParameters):
            response = self._session.get(url, headers=headers, proxies=proxies)
        else:
            response = self._session.get(
                url, queryParameters=queryParameters, headers=headers, proxies=proxies)
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
