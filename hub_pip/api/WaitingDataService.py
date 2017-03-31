import json
import time

from hub_pip.api.CodeLocationsDataService import CodeLocationsDataService
from hub_pip.api.ProjectDataService import ProjectDataService
from hub_pip.api.RestConnection import RestConnection
from hub_pip.api.ScanSummaryDataService import ScanSummaryDataService


class WaitingDataService(object):

    rest_connection = None
    config = None

    def __init__(self, rest_connection, config):
        self.rest_connection = rest_connection
        self.config = config

    def wait_for_project(self, project_name, project_version_name):
        rest_connection = self.rest_connection
        project_data_service = ProjectDataService(rest_connection)
        project_version_view = None
        hub_timeout = time.time() + self.config.hub_server_config.hub_timeout
        while project_version_view is None and time.time() < hub_timeout:
            project_version_view = project_data_service.get_project_version_view(
                project_name, project_version_name)
            if project_version_view is None:
                time.sleep(2)
        if project_version_view is None:
            raise Exception("The hub timed out on project creation")
        return project_version_view

    def wait_for_scan(self, project_version_view):
        rest_connection = self.rest_connection
        code_location_data_service = CodeLocationsDataService(rest_connection)
        hub_timeout = time.time() + self.config.hub_server_config.hub_scan_timeout

        print("Looking for pending scan")
        scans = []
        while scans == [] and time.time() < hub_timeout:
            scans = self.get_pending_scans(project_version_view)
            time.sleep(0.5)
        print("Found " + str(len(scans)) +
              " pending scan(s). Waiting for them to finish")

        while scans != [] and time.time() < hub_timeout:
            scans = self.get_pending_scans(project_version_view)
            time.sleep(0.5)
        print("Pending scans finished")

    def get_pending_scans(self, project_version_view):
        rest_connection = self.rest_connection
        code_location_data_service = CodeLocationsDataService(rest_connection)
        scan_summary_data_service = ScanSummaryDataService(rest_connection)
        scan_links = []

        paged_code_locations = code_location_data_service.get_paged_code_location_view(
            project_version_view)
        for code_location_view in paged_code_locations.items:
            if code_location_view.type == "BOM_IMPORT":
                paged_scan_summary_view = scan_summary_data_service.get_paged_scan_summary_view(
                    code_location_view)
                for scan_summary_view in paged_scan_summary_view.items:
                    if scan_summary_view.status != "COMPLETE":
                        scan_links.append(scan_summary_view.metadata.href)
        return scan_links
