import json

from HubApi import HubApi
from model.PagedView import PagedView
from model.ProjectView import ProjectView


class ProjectDataService(object):

    hub_api = None

    def __init__(self, hub_api):
        self.hub_api = hub_api

    def get_paged_project_view(self, project_name):
        api = self.hub_api
        path = "api/projects"
        params = {
            "q": "name:" + project_name
        }
        response = api.make_get_request(path, params=params)
        response.raise_for_status()
        paged_project_view = response.json()
        paged_project_view = api.remap_object(paged_project_view, PagedView)
        return paged_project_view
