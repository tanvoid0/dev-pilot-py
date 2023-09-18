from py_helper.models.exception_model import ExceptionModel
from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.processor.commander import Commander


class MavenScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Maven Commands",
            [
                OptionModel("mci", "Maven Clean Install", "mvn clean install", self.clean_install),
                OptionModel("mcit", "Maven Clean Install without Tests", "mvn clean install -DskipTests=true",
                            self.clean_install_without_tests),
                OptionModel("mt", "Maven Test", "mvn run test", self.test)
            ]
        )

    def clean_install(self):
        try:
            active_project = ProjectModel.find_active_project()
            Commander.execute_externally(f"cd {active_project.path} && mvn clean install")

        except ExceptionModel as ex:
            ex.print()

    def clean_install_without_tests(self):
        try:
            active_project = ProjectModel.find_active_project()
            Commander.execute_externally(f"cd {active_project.path} && mvn clean install -DskipTests=true")
        except ExceptionModel as ex:
            ex.print()

    def test(self):
        try:
            active_project = ProjectModel.find_active_project()
            Commander.execute_externally(f"cd {active_project.path} && mvn run test")
        except ExceptionModel as ex:
            ex.print()
