import json

from model.PagedProjectView import PagedProjectView
from model.ProjectView import ProjectView
from RestConnection import RestConnection


class ProjectDataService(object):

    rest_connection = None

    def __init__(self, rest_connection):
        self.rest_connection = rest_connection

    def get_paged_project_view(self, project_name):
        api = self.rest_connection
        path = "api/projects"
        params = {
            "q": "name:" + project_name
        }
        response = api.make_get_request(path, params=params)
        response.raise_for_status()
        paged_project_view = response.json()
        paged_project_view = api.remap_object(paged_project_view, PagedProjectView)
        return paged_project_view
