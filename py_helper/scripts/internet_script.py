from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.utility.command_string_generator import CommandStringGenerator


class InternetScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Internet Utilities",
            [
                OptionModel(
                    "i1", "Ping Utility", "e.g., ping google.com", InternetScript.ping
                ),
                OptionModel(
                    "i2",
                    "Kill Port Utility",
                    "e.g., npx kill-port 8080",
                    InternetScript.kill_port,
                ),
                OptionModel(
                    "i3",
                    "open text",
                    "",
                    self.launch_notepad,
                ),
            ],
        )

    @staticmethod
    def ping():
        data = Commander.persistent_input("Enter domain/ip")
        Commander.execute_shell(CommandStringGenerator.ping(data))

    @staticmethod
    def kill_port():
        data = Commander.persistent_input("Enter port to kill")
        Commander.execute_shell(f"npx kill-port {data}")

    @staticmethod
    def launch_notepad():
        Commander.execute_shell(
            "xdg-open /home/tan/Documents/config/dev-pilot-py/kube-configs/payment-service/payment-service-config-2023-09-29-19-31-48.yaml")
