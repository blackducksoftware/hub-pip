import json

from bdsplugin.api.RestConnection import RestConnection
from bdsplugin.api.model.PagedCodeLocationView import PagedCodeLocationView


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

        response = rest_connection.make_get_request_link(code_location_link)
        response.raise_for_status()
        paged_code_location_view = response.json()
        paged_code_location_view = rest_connection.remap_object(
            paged_code_location_view, PagedCodeLocationView)
        return paged_code_location_view
