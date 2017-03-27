import json

from bdsplugin.api.RestConnection import RestConnection
from bdsplugin.api.model.PagedProjectVersionView import \
    PagedProjectVersionView
from bdsplugin.api.model.PagedProjectView import PagedProjectView
from bdsplugin.api.model.ProjectVersionView import ProjectVersionView
from bdsplugin.api.model.ProjectView import ProjectView


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
        paged_project_view = rest_connection.get_paged_from_path(
            PagedProjectView, path, params=params)
        return paged_project_view

    def get_project_view(self, project_name):
        projects = self.get_paged_project_view(project_name)
        if projects.total_count < 1:
            raise Exception("Project not found in the hub")
        return projects.items[0]

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

    def get_project_version_view(self, project_name, project_version_name):
        project_view = self.get_project_view(project_name)
        project_version_views = self.get_paged_version_view(project_view)
        project_version_view = None
        if project_version_views.items:
            for version_view in project_version_views.items:
                if version_view.version_name == project_version_name:
                    project_version_view = version_view
                    break
        return project_version_view
