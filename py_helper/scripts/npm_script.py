from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.models.runtime_var_model import RuntimeVarModel
from py_helper.processor.commander import Commander


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

    def install(self):
        active_project = ProjectModel.find_active_project()
        Commander.execute_externally(f"cd {active_project.path} && npm install")
        # Commander.execute_externally("npm install")

    def clean_install(self):
        active_project = ProjectModel.find_active_project()
        Commander.execute_externally(f"cd {active_project.path} && npm ci")

    def start(self):
        active_project = ProjectModel.find_active_project()
        Commander.execute_externally(f"cd {active_project.path} && npm run start")

    def test(self):
        active_project = ProjectModel.find_active_project()
        Commander.execute_externally(f"cd {active_project.path} && npm run test")

    def lint(self):
        active_project = ProjectModel.find_active_project()
        Commander.execute_externally(f"cd {active_project.path} && npm run lint")

    def build(self):
        active_project = ProjectModel.find_active_project()
        Commander.execute_externally(f"cd {active_project.path} && npm run build")
