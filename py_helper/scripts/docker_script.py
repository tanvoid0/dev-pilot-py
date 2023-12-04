from py_helper.models.exception.app_exception import AppException
from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.service.config_service import ConfigService
from py_helper.service.project_service import ProjectService
from py_helper.service.string_generator.docker_command_string_generator import DockerCommandStringGenerator


class DockerScript(OptionGroupModel):
    config_service = ConfigService()
    project_service = ProjectService()

    def __init__(self):
        super().__init__(
            "Docker Commands",
            [
                OptionModel("db", "Docker Build", "builds docker image",
                            lambda: self.build()),
                OptionModel("dp", "Docker Push", "pushes docker image to cloud",
                            lambda: self.push())
            ]
        )

    def auto_pilot(self):
        active_project = self.project_service.find_active_project()
        config = self.config_service.get_config()
        if active_project is None:
            return []
        else:
            return [
                DockerCommandStringGenerator.build(active_project.path, config.get_docker_image_for_active_project()),
                DockerCommandStringGenerator.push(active_project.path, config.get_docker_image_for_active_project())
            ]

    def build(self, external=True):
        try:
            config = self.config_service.get_config()
            active_project = self.project_service.find_active_project()
            image_tag = config.get_docker_image_for_active_project()
            cmd = DockerCommandStringGenerator.build(active_project.path, image_tag)
            # f"cd {active_project.path} && docker build --network=host --tag {active_project.docker_pre_tag}/{active_project.name}:{active_project.docker_post_tag} ."
            if external:
                Commander.execute_shell(cmd)
            else:
                Commander.execute(cmd)
        except AppException as ex:
            ex.print()

    def push(self, external=True):
        try:
            config = self.config_service.get_config()
            active_project = self.project_service.find_active_project()
            image_tag = config.get_docker_image_for_active_project()
            cmd = DockerCommandStringGenerator.push(active_project.path, image_tag)
            #     f"cd {active_project.path} && docker push "
            # f"{active_project.docker_pre_tag}/{active_project.name}:{active_project.docker_post_tag}"
            if external:
                Commander.execute_shell(cmd)
            else:
                Commander.execute(cmd)
        except AppException as ex:
            ex.print()
