from HubApi import HubApi

class AuthenticationDataService(object):

    hub_api = None

    def __init__(self, hub_api):
        self.hub_api = hub_api

    def authenticate(self):
        # Sprinkle cookies into the session
        credentials = {
            "j_username": self.hub_api.config.hub_username,
            "j_password": self.hub_api.config.hub_password
        }
        response = self.hub_api.make_post_request(self.hub_api.JSPRING, credentials)
        return response
