class ProjectVersionView(object):

    distribution = None
    license = None
    nickname = None
    phase = None
    release_comments = None
    released_on = None
    source = None
    version_name = None
    metadata = None

    attribute_map = {
        "distribution": "distribution",
        "license": "license",
        "nickname": "nickname",
        "phase": "phase",
        "release_comments": "releaseComments",
        "released_on": "releasedOn",
        "source": "source",
        "version_name": "versionName",
        "metadata": "_metadata"
    }

    def __init__(self):
        pass
