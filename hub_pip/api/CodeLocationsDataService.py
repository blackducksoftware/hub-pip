import json

from hub_pip.api.RestConnection import RestConnection
from hub_pip.api.model.PagedCodeLocationView import PagedCodeLocationView


class CodeLocationsDataService(object):

    rest_connection = None

    def __init__(self, rest_connection):
        self.rest_connection = rest_connection

    def get_paged_code_location_view(self, project_version_view):
        rest_connection = self.rest_connection
        code_location_link = None
        for link in project_version_view.metadata.links:
            if link["rel"] == "codelocations":
                code_location_link = link["href"]
                break
        if code_location_link is None:
            raise Exception(
                "codelocation metadata not found in project version view")

        paged_code_location_view = rest_connection.get_view_from_link(
            PagedCodeLocationView, code_location_link)
        return paged_code_location_view
