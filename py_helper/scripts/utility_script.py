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
                OptionModel("encode", "Base64 Ecode", "", UtilityScript.encode),
                OptionModel("decode", "Base64 Decode", "", UtilityScript.decode),
                OptionModel("diff", "Diff Checker", "", UtilityScript.diff_checker),
                OptionModel("note", "Open Notepad", "", self.open_with_notepad),
                OptionModel("run", "Run custom command", "e.g., echo 'Hello World'", UtilityScript.custom_command),
                OptionModel("bot", "Run AI Bot", "", self.run_bot),
            ]
        )

    @staticmethod
    def decode(args):
        if args is None:
            data = Commander.persistent_input("Enter Base64 String to decode")
        else:
            data = args[0]
        print(Base64Util.decode(data))

    @staticmethod
    def encode(args):
        if args is None:
            data = Commander.persistent_input("Enter String to encode to Base64")
        else:
            data = args[0]
        output = Base64Util.encode(data)
        print(output)

    @staticmethod
    def diff_checker(args):
        Commander.execute_python(args=['run=diff_checker'])

    def open_with_notepad(self, args):
        file_path = None
        if args is not None:
            file_path = args[0]
        self.file_processor.reader.read(file_path, with_notepad=True)

    @staticmethod
    def custom_command(args):
        if args is None:
            data = Commander.persistent_input("Enter your custom command")
        else:
            data = args.join(" ")
        Commander.execute_shell(f"{data}")

    @staticmethod
    def run_bot(args):
        if args is None:
            args = ['run=bot']
        Commander.execute_python(args=args)
