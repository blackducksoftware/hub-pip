import requests

from HubServerConfig import HubServerConfig


class HubApi(object):

    JSPRING = "/j_spring_security_check"

    _session = None
    config = None

    def __init__(self, hub_server_config):
        self._session = requests.session()
        if isinstance(hub_server_config, HubServerConfig):
            self.config = hub_server_config

    def _authenticate(self):
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
        url = config.hub_url + path
        response = None
        if(queryParameters):
            response = self._session.get(url)
        else:
            response = self._session.get(url, queryParameters)
        return response

    def make_post_request(self, path, content):
        """
        path: str
        content: str or dict
        """
        url = config.hub_url + path
        response = self._session.post(url, content)
        return response
