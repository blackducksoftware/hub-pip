from hub_pip.api.model.NameValuePair import NameValuePair


class VersionBomPolicyStatusView(object):

    component_version_status_counts = None
    overall_status = None
    updated_at = None

    attribute_map = {
        'component_version_status_counts': 'componentVersionStatusCounts',
        'overall_status': 'overallStatus',
        'updated_at': 'updatedAt'
    }

    attribute_schema = {
        "component_version_status_counts": [NameValuePair]
    }

    def __init__(self):
        pass

    def get_in_violation(self):
        return self._get_value("IN_VIOLATION")

    def get_in_violation_but_overridden(self):
        return self._get_value("IN_VIOLATION_OVERRIDDEN")

    def get_not_in_violation(self):
        return self._get_value("NOT_IN_VIOLATION")

    def _get_value(self, value_name):
        for count_pair in self.component_version_status_counts:
            if count_pair.name == value_name:
                return str(count_pair.value)
        return "0"  # No components were found
