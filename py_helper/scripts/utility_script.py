from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.processor.file.file_processor import FileProcessor
from py_helper.utility.base64util import Base64Util


class UtilityScript(OptionGroupModel):
    file_processor = FileProcessor()

    def __init__(self):
        super().__init__(
            "Useful Utilities",
            [
                OptionModel("u1", "Base64 Ecode", "", UtilityScript.encode),
                OptionModel("u2", "Base64 Decode", "", UtilityScript.decode),
                OptionModel("diff", "Diff Checker", "", UtilityScript.diff_checker),
                OptionModel("note", "Open Notepad", "", self.open_with_notepad),
                OptionModel("c", "Run custom command", "e.g., echo 'Hello World'", UtilityScript.custom_command),
            ]
        )

    @staticmethod
    def decode():
        data = Commander.persistent_input("Enter Base64 String to decode")
        print(Base64Util.decode(data))

    @staticmethod
    def encode():
        data = Commander.persistent_input("Enter String to encode to Base64")
        print(Base64Util.encode(data))

    @staticmethod
    def diff_checker():
        Commander.execute_python(args=['run=diff_checker'])

    def open_with_notepad(self):
        self.file_processor.reader.read(None, with_notepad=True)

    @staticmethod
    def custom_command():
        data = Commander.persistent_input("Enter your custom command")
        Commander.execute_shell(f"{data}")
