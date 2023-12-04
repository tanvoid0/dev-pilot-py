from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.service.string_generator.gcloud_command_string_generator import GCloudCommandStringGenerator


class GcloudScript(OptionGroupModel):
    def __int__(self):
        super().__init__(
            "GCloud Commands",
            [
                OptionModel("gcpl", "GCloud Login", "gcloud auth login", self.login),
                OptionModel("gcpi", "GCloud Init", "gcloud init", self.init)
            ],
        ),

    @staticmethod
    def login():
        Commander.execute_shell(GCloudCommandStringGenerator.login())

    @staticmethod
    def init():
        Commander.execute_shell(GCloudCommandStringGenerator.init_gcloud())
