import json

from bdsplugin.api.model.PagedProjectVersionView import \
    PagedProjectVersionView
from bdsplugin.api.model.PagedProjectView import PagedProjectView
from bdsplugin.api.model.ProjectVersionView import ProjectVersionView
from bdsplugin.api.model.ProjectView import ProjectView
from bdsplugin.api.RestConnection import RestConnection


class ProjectDataService(object):

    rest_connection = None

    def __init__(self, rest_connection):
        self.rest_connection = rest_connection

    def get_paged_project_view(self, project_name):
        rest_connection = self.rest_connection
        path = "api/projects"
        params = {
            "q": "name:" + project_name
        }
        response = rest_connection.make_get_request(path, params=params)
        response.raise_for_status()
        paged_project_view = response.json()
        paged_project_view = rest_connection.remap_object(paged_project_view, PagedProjectView)
        if paged_project_view.total_count < 1:
            raise Exception("Project not found in the hub")
        return paged_project_view

    def get_paged_version_view(self, project_view):
        rest_connection = self.rest_connection
        version_link = None
        for link in project_view.metadata.links:
            if link["rel"] == "versions":
                version_link = link["href"]
                break
        if version_link is None:
            raise Exception("No metadata found in project view")

        response = rest_connection.make_get_request_link(version_link)
        response.raise_for_status()
        paged_project_version_view = response.json()
        paged_project_version_view = rest_connection.remap_object(
            paged_project_version_view, PagedProjectVersionView)
        return paged_project_version_view
