from bdsplugin.api.RestConnection import RestConnection


class LinkedDataDataService(object):

    rest_connection = None

    def __init__(self, rest_connection):
        self.rest_connection = rest_connection

    def upload_bdio(self, bdio):
        path = "api/bom-import"
        url = self.rest_connection.build_url(path)
        headers = self.rest_connection.headers_jsonld()
        proxies = self.rest_connection.get_proxies()
        response = self.rest_connection._session.post(url, bdio, headers=headers, proxies=proxies)
        return response
