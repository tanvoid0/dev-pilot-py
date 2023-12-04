from py_helper.processor.commander import Commander
from py_helper.service.config_service import ConfigService
from py_helper.utility.command_string_generator import CommandStringGenerator


class KubernetesScaleService:
    config_service = ConfigService()

    def scale_deployment(self, deployment_name, down=False, stateful_set=False):
        config = self.config_service.get_config()
        Commander.execute_shell(
            CommandStringGenerator.kubernetes_scale(config.namespace, deployment_name, down, stateful_set))
