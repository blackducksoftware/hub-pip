from hub_pip.tests.helper import *


class TestConfig:

    def test_valid(self):
        config = get_config(VALID)
        assert(config.hub_server_config.hub_username == None)

    def test_invalid(self):
        config = get_config(INVALID)
        assert(config.hub_server_config.hub_username != None)

    def test_broken(self):
        broken = False
        try:
            config = get_config(BROKEN)
        except Exception:
            broken = True
        assert(broken)
