import requests

from HubServerConfig import HubServerConfig

JSPRING = "/j_spring_security_check"


class HubApi(object):

    _session = None
    config = None  # HubServerConfig

    def __init__(self, hub_server_config):
        self._session = requests.session()
        if isinstance(hub_server_config, HubServerConfig):
            self.config = hub_server_config

    def authenticate(self):
        # Sprinkle cookies into the session
        content = {
            "j_username": self.config.hub_username,
            "j_password": self.config.hub_password
        }
        self.make_post_request(JSPRING, content)

    def make_get_request(self, path, queryParameters=None):
        """
        path: str
        queryParameters: dict
        """
        url = self.build_url(path)
        response = None
        if(queryParameters):
            response = self._session.get(url)
        else:
            response = self._session.get(url, queryParameters)
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

    def build_url(self, path):
        url = "{}/{}".format(self.config.hub_url, path)
        return url

    def upload_bdio(self, bdio):
        path = "api/bom-import"
        url = self.build_url(path)
        response = self._session.post(url, bdio, headers=self.headers_jsonld())
        return response
