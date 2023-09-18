from py_helper.models.exception_model import ExceptionModel
from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.processor.commander import Commander


class DockerScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Docker Commands",
            [
                OptionModel("db", "Docker Build", "builds docker image", self.build),
                OptionModel("dp", "Docker Push", "pushes docker image to cloud", self.push)
            ]
        )

    @staticmethod
    def build():
        try:
            active_project = ProjectModel.find_active_project()

            Commander.execute_externally(
                f"cd {active_project.path} && docker build --network=host --tag "
                f"{active_project.docker_pre_tag}/{active_project.docker_name}:{active_project.docker_post_tag} .")
        except ExceptionModel as ex:
            ex.print()

    @staticmethod
    def push():
        try:
            active_project = ProjectModel.find_active_project()
            Commander.execute_externally(f"cd {active_project.path} && docker push "
                                         f"{active_project.docker_pre_tag}/{active_project.docker_name}:{active_project.docker_post_tag}")
        except ExceptionModel as ex:
            ex.print()
