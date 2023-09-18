from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander


class GcloudScript(OptionGroupModel):
    def __int__(self):
        super().__init__(
            "GCloud Commands",
            [
                OptionModel("gcpl", "GCloud Login", "gcloud auth login", self.login),
                OptionModel("gcpi", "GCloud Init", "gcloud init", self.init)
            ],
        ),

    def login(self):
        Commander.execute_externally("gcloud auth login")

    def init(self):
        Commander.execute_externally("gcloud init")
