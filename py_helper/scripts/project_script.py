from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.service.project_service import ProjectService


class ProjectScript(OptionGroupModel):
    project_service = ProjectService()

    def __init__(self):
        super().__init__(
            "Project Utilities",
            [
                OptionModel(
                    "ps", "Project Show", "", self.project_service.show
                ),
                OptionModel(
                    "pi",
                    "Project Insert",
                    "Creates a Project Item",
                    self.add_project,
                ),
                OptionModel("0", "Open Autopilot", "Beta", lambda: self.autopilot(), ),
            ],
        )

    @staticmethod
    def autopilot():
        Commander.execute_python(args=["pilot=PROJECT,DOCKER,KUBERNETES"])

    def add_project(self):
        self.project_service.add_project()
