from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.service.project_service import ProjectService
from py_helper.service.string_generator.flutter_command_string_generator import FlutterCommandStringGenerator


class FlutterScript(OptionGroupModel):
    project_service = ProjectService()

    def __init__(self):
        super().__init__(
            "Flutter Scripts",
            [
                OptionModel(
                    "fg",
                    "Pub Get Packages",
                    "",
                    lambda: self.pub_get_packages()
                ),
                OptionModel(
                    "fd",
                    "Flutter Doctor",
                    "",
                    lambda: self.doctor()
                ),
                OptionModel(
                    "fcb",
                    "Flutter Clean Build Models",
                    "",
                    lambda: self.clean_build_models()
                ),
            ]
        )

    @staticmethod
    def doctor():
        Commander.execute_shell(FlutterCommandStringGenerator.doctor())

    def pub_get_packages(self):
        project = self.project_service.find_active_project()
        Commander.execute_shell(FlutterCommandStringGenerator.pub_get_packages(project.path))

    def clean_build_models(self):
        project = self.project_service.find_active_project()
        Commander.execute_shell(FlutterCommandStringGenerator.clean_build_models(project.path))
