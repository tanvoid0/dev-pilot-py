from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.service.project_service import ProjectService
from py_helper.service.string_generator.npm_command_string_generator import NpmCommandStringGenerator


class NpmScript(OptionGroupModel):
    project_service = ProjectService()

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

    def install(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.install(active_project.path))

    def clean_install(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.clean_install(active_project.path))

    def start(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.start(active_project.start))

    def test(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.test(active_project.path))

    def lint(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.lint(active_project.path))

    def build(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(NpmCommandStringGenerator.build(active_project.path))
