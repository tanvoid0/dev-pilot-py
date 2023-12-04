from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.service.config_service import ConfigService
from py_helper.service.project_service import ProjectService
from py_helper.service.string_generator.maven_command_string_generator import MavenCommandStringGenerator


class MavenScript(OptionGroupModel):
    config_service = ConfigService()
    project_service = ProjectService()
    maven_string = MavenCommandStringGenerator()

    def __init__(self):
        super().__init__(
            "Maven Commands",
            [
                OptionModel("m1", "Maven Clean Install without Tests", "mvn clean install -DskipTests=true",
                            self.clean_install_without_tests),
                OptionModel("m2", "Maven Clean Install", "mvn clean install", self.clean_install),
                OptionModel("m3", "Maven Test", "mvn test", self.test),
                OptionModel("l1", "Liquibase Prepare", "", self.liquibase_prepare_diff),
                OptionModel("l2", "Liquibase Create", "", self.liquibase_create_diff),
                OptionModel("l3", "Liquibase Process", "", self.liquibase_process_diff),
                OptionModel("l4", "Liquibase Validate", "", self.liquibase_verify_diff),

            ]
        )

    def auto_pilot(self):
        return [
            MavenCommandStringGenerator.clean_install(self.project_service.find_active_project().path,
                                                      without_tests=True),
        ]

    def clean_install(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.clean_install(active_project.path))

    def clean_install_without_tests(self, external=True):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.clean_install(active_project.path, without_tests=True),
                                external=external)

    def test(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.test(active_project.path))

    def prepare_pact_test(self):
        # active_project = self.project_service.find_active_project()
        # config_file = self.config_service.get_config_file()
        # Commander.execute_shell(
        #     self.maven_string.prepare_pact_test(active_project.path, config_file.config.maven_username, config_file.config.maven_password) +"; " +
        #     self.maven_string.verify_pact_test(active_project.path, config_file.config.maven.pact_url, config_file.config.maven.pact_branch))
        pass

    def liquibase_prepare_diff(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.liquibase_prepare_for_diff(active_project.path))

    def liquibase_create_diff(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.liquibase_create_diff(active_project.path))

    def liquibase_process_diff(self):
        raise "Function 'liquibase_process_diff' not implemented yet"

    def liquibase_verify_diff(self):
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(MavenCommandStringGenerator.liquibase_verify_diff(active_project.path))
