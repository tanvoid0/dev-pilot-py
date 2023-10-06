from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.processor.commander import Commander


class ProjectScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Project Utilities",
            [
                OptionModel(
                    "ps", "Project Show", "Select Project from List", ProjectModel.show
                ),
                OptionModel(
                    "pi",
                    "Project Insert",
                    "Creates a Project Item",
                    ProjectModel.insert,
                ),
                OptionModel("0", "Open Autopilot", "Beta", lambda: self.autopilot(), ),
            ],
        )

    @staticmethod
    def autopilot():
        Commander.execute_python(args=["pilot=PROJECT,DOCKER,KUBERNETES"])
