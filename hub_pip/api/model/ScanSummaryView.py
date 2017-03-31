from hub_pip.api.model.MetadataView import MetadataView


class ScanSummaryView(object):

    created_at = None
    status = None
    status_message = None
    updated_at = None
    metadata = None

    attribute_map = {
        'created_at': 'createdAt',
        'status': 'status',
        'status_message': 'statusMessage',
        'updated_at': 'updatedAt',
        "metadata": "_meta"
    }

    attribute_schema = {
        "metadata": MetadataView
    }

    def __init__(self):
        pass
