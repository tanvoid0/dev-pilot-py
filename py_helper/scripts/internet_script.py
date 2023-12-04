from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.processor.file.file_processor import FileProcessor
from py_helper.utility.command_string_generator import CommandStringGenerator


class InternetScript(OptionGroupModel):
    file_processor = FileProcessor()

    def __init__(self):
        super().__init__(
            "Internet Utilities",
            [
                OptionModel(
                    "i1", "Ping Utility", "e.g., ping google.com", InternetScript.ping
                ),
                OptionModel(
                    "i2",
                    "Kill Port Utility",
                    "e.g., npx kill-port 8080",
                    InternetScript.kill_port,
                ),
                OptionModel(
                    "i3",
                    "open text",
                    "",
                    self.launch_notepad,
                ),
            ],
        )

    @staticmethod
    def ping():
        data = Commander.persistent_input("Enter domain/ip")
        Commander.execute_shell(CommandStringGenerator.ping(data))

    @staticmethod
    def kill_port():
        data = Commander.persistent_input("Enter port to kill")
        Commander.execute_shell(f"npx kill-port {data}")

    def launch_notepad(self):
        file = self.file_processor.reader.select_file()
        if file is not None:
            Commander.execute_shell(CommandStringGenerator.launch_notepad(file))
