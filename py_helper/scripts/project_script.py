from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel


class ProjectScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Project Utilities",
            [
                OptionModel("ps", "Project Show", "Shows list of projects", ProjectModel.show),
                OptionModel("pi", "Project Insert", "Creates a Project Item", ProjectModel.insert),
                OptionModel("pg", "Project Select", "Find and Select project", ProjectModel.find_by_id)
            ]
        )
