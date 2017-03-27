import json

from bdsplugin.api.RestConnection import RestConnection
from bdsplugin.api.model.PagedScanSummaryView import PagedScanSummaryView


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

        response = rest_connection.make_get_request_link(scan_summary_link)
        response.raise_for_status()
        paged_scan_summary_view = response.json()
        paged_scan_summary_view = rest_connection.remap_object(
            paged_scan_summary_view, PagedScanSummaryView)
        return paged_scan_summary_view
