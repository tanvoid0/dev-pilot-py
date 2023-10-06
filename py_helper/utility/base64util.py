from py_helper.processor.commander import Commander
from py_helper.scripts.string_generator.base_64_command_string_generator import Base64CommandStringGenerator


class Base64Util:
    @staticmethod
    def encode(data):
        return Commander.execute(Base64CommandStringGenerator.encode(data))

    @staticmethod
    def decode(data):
        return Commander.execute(Base64CommandStringGenerator.encode(data))
