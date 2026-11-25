from py_helper.service.config_service import ConfigService
from py_helper.service.project_service import ProjectService
from py_helper.service.string_generator.docker_command_string_generator import DockerCommandStringGenerator
from py_helper.service.string_generator.kubernetes_command_string_generator import KubernetesCommandStringGenerator


class MavenCommandStringGenerator:
    @staticmethod
    def clean_install(path, without_tests=False, deploy=False):
        cmd = f"cd {path} && mvn clean install {'-DskipTests=True' if without_tests else ''}"
        if deploy:
            config = ConfigService().get_config()
            project = ProjectService().find_active_project()
            deployment = project.deployment
            image_tag = config.get_docker_image_for_active_project()
            cmd += " && " + DockerCommandStringGenerator.build_and_push(path, image_tag)
            cmd += " && " + KubernetesCommandStringGenerator.restart(config.namespace,
                                                                     deployment.name,
                                                                     deployment.stateful_set)
        return cmd

    @staticmethod
    def test(path):
        return f'cd {path} && mvn test'

    @staticmethod
    def prepare_pact_test(path: str, username: str, password: str):
        return f"cd {path} && mvn  clean install -U -Dcdcstubs_mode=REMOTE -Dcdcstubs_repo_username=\"{username}\" -Dcdcstubs_repo_password=\"{password}\""

    @staticmethod
    def verify_pact_test(path: str, pact_url: str, branch_name: str = "latest"):
        return f"cd {path} && mvn -PVERIFY test -Dpactbroker.url=\"{pact_url}\" -Dpactbroker.consumerversionselectors.tags={branch_name} -Dpactbroker.consumers={branch_name}"

    @staticmethod
    def liquibase_prepare_for_diff(path: str):
        return f"cd {path} && mvn -PLIQUIBASE_PREPARE_FOR_DIFF test"

    @staticmethod
    def liquibase_create_diff(path: str):
        return f"cd {path} && mvn liquibase:update liquibase:diff"

    @staticmethod
    def liquibase_verify_diff(path: str):
        return f"cd {path} && mvn -PLIQUIBASE_VERIFY test"
