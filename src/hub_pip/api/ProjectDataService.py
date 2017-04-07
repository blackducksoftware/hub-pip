import json

from hub_pip.api.RestConnection import RestConnection
from hub_pip.api.model.PagedProjectVersionView import \
    PagedProjectVersionView
from hub_pip.api.model.PagedProjectView import PagedProjectView
from hub_pip.api.model.ProjectVersionView import ProjectVersionView
from hub_pip.api.model.ProjectView import ProjectView


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
        paged_project_view = rest_connection.get_view_from_path(
            PagedProjectView, path, params=params)
        return paged_project_view

    def get_project_view(self, project_name):
        projects = self.get_paged_project_view(project_name)
        if projects.total_count < 1:
            return None
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
        paged_project_version_view = rest_connection.get_view_from_link(
            PagedProjectVersionView, version_link)
        return paged_project_version_view

    def get_project_version_view(self, project_name, project_version_name):
        project_view = self.get_project_view(project_name)
        if project_view is None:
            return None
        project_version_views = self.get_paged_version_view(project_view)
        project_version_view = None
        if project_version_views.items:
            for version_view in project_version_views.items:
                if version_view.version_name == project_version_name:
                    project_version_view = version_view
                    break
        return project_version_view
