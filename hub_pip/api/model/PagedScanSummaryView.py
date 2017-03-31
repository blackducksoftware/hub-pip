from hub_pip.api.model.ScanSummaryView import ScanSummaryView


class PagedScanSummaryView(object):

    total_count = None
    items = None

    attribute_map = {
        "total_count": "totalCount",
        "items": "items",
    }

    attribute_schema = {
        "items": [ScanSummaryView]
    }

    def __init__(self):
        pass
