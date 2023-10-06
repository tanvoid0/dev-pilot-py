import re

from py_helper.models.exception.exception_model import ExceptionModel
from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.processor.commander import Commander
from py_helper.scripts.string_generator.git_command_string_generator import GitCommandStringGenerator


class GitScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Git Commands",
            [
                OptionModel("gr", "Git remote", "shows remote urls linked to git repository", self.remote),
                OptionModel("gs", "Git Status", "", self.status)
            ]
        )

    def remote(self):
        try:
            active_project = ProjectModel.find_active_project()
            output = Commander.execute(GitCommandStringGenerator.get_remote(active_project.path))
            match = re.search(r"git@(.*?):(.*?)/(.*?)\.git", output)
            if match:
                output = "https://" + match.group(1) + "/" + match.group(2) + "/" + match.group(3)
                print(output)
            else:
                print("No remote url found")
                return None
            input("press enter to continue")
        except ExceptionModel as ex:
            ex.print()

    def status(self):
        try:
            active_project = ProjectModel.find_active_project()
            Commander.execute(GitCommandStringGenerator.status(active_project.path), show=True)
        except ExceptionModel as ex:
            ex.print()
