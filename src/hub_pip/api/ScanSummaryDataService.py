import json

from hub_pip.api.RestConnection import RestConnection
from hub_pip.api.model.PagedScanSummaryView import PagedScanSummaryView


class ScanSummaryDataService(object):

    rest_connection = None

    def __init__(self, rest_connection):
        self.rest_connection = rest_connection

    def get_paged_scan_summary_view(self, code_location_view):
        rest_connection = self.rest_connection
        scan_summary_link = None
        for link in code_location_view.metadata.links:
            if link["rel"] == "scans":
                scan_summary_link = link["href"]
                break
        if scan_summary_link is None:
            raise Exception("scans metadata not found in project version view")

        paged_scan_summary_view = rest_connection.get_view_from_link(
            PagedScanSummaryView, scan_summary_link)
        return paged_scan_summary_view
