from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander


class InternetScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Internet Utilities",
            [
                OptionModel("i1", "Ping Utility", "e.g., ping google.com", InternetScript.ping),
                OptionModel("i2", "Kill Port Utility", "e.g., npx kill-port 8080", InternetScript.kill_port),
                OptionModel("0", "Open Autopilot", "Beta", self.autopilot)
            ]
        )

    @staticmethod
    def ping():
        data = Commander.persistent_input("Enter ip address or host to ping")
        Commander.execute_externally(f"ping {data}")

    @staticmethod
    def kill_port():
        data = Commander.persistent_input("Enter port to kill")
        Commander.execute_externally(f"npx kill-port {data}")

    def autopilot(self):
        Commander.execute_python()
