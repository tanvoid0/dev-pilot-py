from py_helper.models.option_model import OptionModel, OptionGroupModel
from py_helper.processor.commander import Commander


class AutoPilotScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Autopilot",
            [
                OptionModel("0", "Open Autopilot", "Beta", self.autopilot),
            ],
        )

    @staticmethod
    def autopilot():
        Commander.execute_python(args=["test script", "x=y", "z", "a=bc"])
