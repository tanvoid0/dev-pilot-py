from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.processor.commander import Commander
from py_helper.scripts.string_generator.npm_command_string_generator import NpmCommandStringGenerator


class NpmScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Npm Commands",
            [
                OptionModel("ni", "Npm install", "npm install", self.install),
                OptionModel("nc", "Npm Clean Install", "npm ci", self.clean_install),
                OptionModel("ns", "Npm Start", "npm run start", self.start),
                OptionModel("nt", "Npm test", "npm run test", self.test),
                OptionModel("nl", "Npm Lint check", "npm run lint", self.lint),
                OptionModel("nb", "Npm Build", "npm run build", self.build),
            ]
        )

    @staticmethod
    def install():
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.install(active_project.path))

    @staticmethod
    def clean_install():
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.clean_install(active_project.path))

    @staticmethod
    def start():
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.start(active_project.start))

    @staticmethod
    def test():
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.test(active_project.path))

    @staticmethod
    def lint():
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.lint(active_project.path))

    @staticmethod
    def build():
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.build(active_project.path))
