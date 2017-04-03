from hub_pip.api.RestConnection import RestConnection


class AuthenticationDataService(object):

    rest_connection = None

    def __init__(self, rest_connection):
        self.rest_connection = rest_connection

    def authenticate(self):
        # Sprinkle cookies into the session
        credentials = {
            "j_username": self.rest_connection.config.hub_username,
            "j_password": self.rest_connection.config.hub_password
        }
        response = self.rest_connection.make_post_request(
            self.rest_connection.JSPRING, credentials)
        response.raise_for_status()
        return response


def get_authenticated_api(hub_server_config):
    rc = RestConnection(hub_server_config)
    authentication_data_service = AuthenticationDataService(rc)
    authentication_response = authentication_data_service.authenticate()
    authentication_response.raise_for_status()
    return rc
