import os

from hub_pip.BlackDuckCore import BlackDuckCore
from hub_pip.FileHandler import get_file_path, BDIO_EXTENSION
from hub_pip.tests.helper import *
import pip


class TestDeployment:

    def test_deployment(self):
        config = get_config(VALID)
        # config.requirements_file_path = REQUIREMENTS
        config.create_hub_bdio = True
        config.deploy_hub_bdio = True

        core = BlackDuckCore(config)
        tree = core.run()

        bdio_file_name = get_file_path(
            "hub-pip", config.output_path, BDIO_EXTENSION)
        assert(os.path.exists(bdio_file_name))
        cleanup(bdio_file_name)

        policy_status = core.check_policies(tree)
        assert(policy_status.get_in_violation() == "0")
        assert(policy_status.get_in_violation_but_overridden() == "0")
        assert(policy_status.get_not_in_violation() == "4")
