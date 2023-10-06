from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.processor.commander import Commander
from py_helper.scripts.string_generator.maven_command_string_generator import MavenCommandStringGenerator


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

    @staticmethod
    def auto_pilot():
        path = ProjectModel.find_active_project().path
        return [
            MavenCommandStringGenerator.clean_install(path, without_tests=True),
        ]

    @staticmethod
    def clean_install():
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.clean_install(active_project.path))

    @staticmethod
    def clean_install_without_tests(external=True):
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.clean_install(active_project.path, without_tests=True),
                                external=external)

    @staticmethod
    def test():
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.test(active_project.path))
