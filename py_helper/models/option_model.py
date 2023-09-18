from typing import Callable

from py_helper.processor.print_processor import color_text, BRED_TEXT, BWHITE_TEXT, BLUE_TEXT, BPURPLE_TEXT


class OptionModel:
    choice: str
    title: str
    command_example: str
    method: Callable

    def __init__(self, choice, title, command_example, method):
        self.choice = choice
        self.title = title
        self.command_example = command_example
        self.method = method

    def option_text(self):
        return f"{color_text(BRED_TEXT, self.choice)}. {color_text(BWHITE_TEXT, self.title)} {color_text(BLUE_TEXT, self.command_example)}\n"


class OptionGroupModel:
    title: str
    commands: [OptionModel]

    def __init__(self, title, commands):
        self.title = title
        self.commands = commands

    def print_option(self):
        data = color_text(BPURPLE_TEXT, self.title) + "\n"

        for value in self.commands:
            data += value.option_text()

        data += "\n"

        return data

    def run_option(self, option):
        for value in self.commands:
            if value.choice == option:
                value.method()
                return
        print("No option found")
