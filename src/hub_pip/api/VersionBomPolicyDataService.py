import json

from hub_pip.api.RestConnection import RestConnection
from hub_pip.api.model.VersionBomPolicyStatusView import VersionBomPolicyStatusView


class VersionBomPolicyDataService(object):

    rest_connection = None

    def __init__(self, rest_connection):
        self.rest_connection = rest_connection

    def get_version_bom_policy_view(self, project_version_view):
        rest_connection = self.rest_connection
        policy_status_link = None
        for link in project_version_view.metadata.links:
            if link["rel"] == "policy-status":
                policy_status_link = link["href"]
                break
        if policy_status_link is None:
            raise Exception("No metadata found in project version view")

        version_bom_policy_view = rest_connection.get_view_from_link(
            VersionBomPolicyStatusView, policy_status_link)
        return version_bom_policy_view
