from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel


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
            ],
        )
