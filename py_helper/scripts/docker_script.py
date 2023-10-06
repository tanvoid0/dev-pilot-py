from py_helper.models.exception.exception_model import ExceptionModel
from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.processor.commander import Commander
from py_helper.scripts.string_generator.docker_command_string_generator import DockerCommandStringGenerator


class DockerScript(OptionGroupModel):
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

    @staticmethod
    def auto_pilot():
        active_project = ProjectModel.find_active_project()
        return [
            DockerCommandStringGenerator.build(active_project.path, active_project.image_name),
            DockerCommandStringGenerator.push(active_project.path, active_project.image_name)
        ]

    @staticmethod
    def build(external=True):
        try:
            active_project = ProjectModel.find_active_project()
            cmd = DockerCommandStringGenerator.build(active_project.path, active_project.image_name)
            # f"cd {active_project.path} && docker build --network=host --tag {active_project.docker_pre_tag}/{active_project.name}:{active_project.docker_post_tag} ."
            if external:
                Commander.execute_shell(cmd)
            else:
                Commander.execute(cmd)
        except ExceptionModel as ex:
            ex.print()

    @staticmethod
    def push(external: True):
        try:
            active_project = ProjectModel.find_active_project()
            cmd = DockerCommandStringGenerator.push(active_project.path,
                                                    f"{active_project.docker_pre_tag}/{active_project.name}:{active_project.docker_post_tag}")
            #     f"cd {active_project.path} && docker push "
            # f"{active_project.docker_pre_tag}/{active_project.name}:{active_project.docker_post_tag}"
            if external:
                Commander.execute_shell(cmd)
            else:
                Commander.execute(cmd)
        except ExceptionModel as ex:
            ex.print()
