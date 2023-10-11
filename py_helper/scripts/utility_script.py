from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander


class UtilityScript(OptionGroupModel):

    def __init__(self):
        super().__init__(
            "Useful Utilities",
            [
                OptionModel("b64e", "Base64 Ecode", "e.g., echo '$1' | base64", UtilityScript.encode),
                OptionModel("b64d", "Base64 Decode", "e.g., echo '$1' | base64 --decode", UtilityScript.decode),
                OptionModel("c", "Run custom command", "e.g., echo 'Hello World'", UtilityScript.custom_command)
            ]
        )

    @staticmethod
    def decode():
        data = Commander.persistent_input("Enter Base64 String to decode")
        Commander.execute(f"echo '{data}' | base64 --decode", show=True)

    @staticmethod
    def encode():
        data = Commander.persistent_input("Enter String to encode to Base64")
        Commander.execute(f"echo '{data}' | base64", show=True)

    @staticmethod
    def custom_command():
        data = Commander.persistent_input("Enter your custom command")
        Commander.execute_shell(f"{data}")
