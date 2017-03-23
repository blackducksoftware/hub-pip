from HubApi import HubApi

class LinkedDataDataService(object):

    hub_api = None

    def __init__(self, hub_api):
        self.hub_api = hub_api

    def upload_bdio(self, bdio):
        path = "api/bom-import"
        url = self.hub_api.build_url(path)
        headers = self.hub_api.headers_jsonld()
        proxies = self.hub_api.get_proxies()
        response = self.hub_api._session.post(url, bdio, headers=headers, proxies=proxies)
        return response
