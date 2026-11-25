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
                    "ping", "Ping Utility", "e.g., ping google.com", InternetScript.ping
                ),
                OptionModel(
                    "kill-port",
                    "Kill Port Utility",
                    "e.g., kill-port 8080",
                    InternetScript.kill_port,
                ),
                OptionModel(
                    "open",
                    "open text",
                    "",
                    self.launch_notepad,
                ),
            ],
        )

    @staticmethod
    def ping(args):
        if args is None or len(args) == 0:
            data = Commander.persistent_input("Enter domain/ip")
        else:
            data = args[0]
        Commander.execute_shell(CommandStringGenerator.ping(data))

    @staticmethod
    def kill_port(args):
        if args is None or len(args) == 0:
            data = Commander.persistent_input("Enter port to kill")
        else:
            data = args[0]
        Commander.execute_shell(f"npx kill-port {data}")

    def launch_notepad(self, args):
        if args is None or len(args) == 0:
            file = self.file_processor.reader.select_file()
        else:
            file = args[0]
        if file is not None:
            Commander.execute_shell(CommandStringGenerator.launch_notepad(file))
