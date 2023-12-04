import os
import subprocess
import webbrowser

import pandas as pd
from tabulate import tabulate

from py_helper.processor.os_commander import OSCommander
from py_helper.processor.print_processor import color_text, GREEN_TEXT
from py_helper.utility.command_string_generator import CommandStringGenerator


def empty_string(data):
    return data is None or data.strip() == ""


class Commander:
    def get_terminal_name(self):
        return OSCommander.run(
            linux=lambda: "gnome-terminal",
        )

    @staticmethod
    def execute(commands, show=False, sync=False):
        if sync:
            subprocess.run(commands, shell=True)

        else:
            process = subprocess.run(commands, capture_output=True, shell=True)
            output = process.stdout.decode("utf-8")
            if show:
                print(output)
            return output

    @staticmethod
    def execute_externally(command_to_run, python=False):
        """This is deprecated"""
        Commander.execute_shell(command_to_run)
        # subprocess.run(["python", "exec.py"])
        # if python:
        #     command_to_run = f"python exec.py -k {command_to_run}"
        # else:
        # execute_script_file_path = os.path.join(os.path.abspath(os.getcwd()), "exec.sh")

        # subprocess.Popen([execute_script_file_path, command_to_run], shell=True)

        ### Frozen input
        # output = subprocess.run(
        #     [execute_script_file_path, command_to_run],
        #     shell=True,
        #     stdout=subprocess.PIPE,
        #     text=True,
        # )
        # print("Executing Command {}".format(command_to_run))
        # subprocess.Popen(['x-terminal-emulator', '-e', 'bash', '-c', 'exec.sh', 'echo "Hello from shell script"'])

        # output = subprocess.Popen(['x-terminal-emulator', '-e', 'bash', 'exec.sh', command_to_run], shell=True,
        #                           stdout=subprocess.PIPE, text=True)
        # print("Finished")
        # print(output.stdout)

    @staticmethod
    def execute_shell(command, external=True):
        if not external:
            Commander.execute(command)
        else:
            exec_file = os.path.join(os.getcwd(), "exec.sh")
            OSCommander.run(
                linux=lambda: subprocess.Popen(
                    ["gnome-terminal", "--", exec_file, command],
                    cwd=os.getcwd(),
                ),
                windows=lambda: subprocess.Popen(
                    ["cmd.exe", "/c", "start", exec_file, command],
                    cwd=os.getcwd()
                )
            )

    @staticmethod
    def execute_python(execute=None, args=None, sync=False):
        print(os.getcwd())
        if args is None:
            args = []
            if sync:
                args.append("sync")
        OSCommander.run(
            windows=lambda: (
                subprocess.Popen(
                    ["start", "cmd", "/k", "python", "pilot.py", "" if execute is None else f"exec='{execute}'"] + args,
                    shell=True,
                )
            ),
            linux=lambda: (
                subprocess.Popen(
                    ["gnome-terminal", "--", "python3", "pilot.py", f"exec='{execute}'"] + args,
                    cwd=os.getcwd(),
                )
            )
        )

    @staticmethod
    def open_url(url: str):
        webbrowser.open(url, new=0, autoraise=True)

    @staticmethod
    def print(commands):
        print(Commander.execute(commands))

    @staticmethod
    def print_table(data):
        df = pd.DataFrame(data)
        table = tabulate(df, headers="keys", tablefmt="pretty")
        print(table)

    @staticmethod
    def persistent_input(query, optional_data=None):
        query += (
                     " (default: " + (color_text(GREEN_TEXT, optional_data) + ")")
                     if optional_data is not None
                     else ""
                 ) + ": "
        while True:
            data = input(query)
            # query + ("(" + color_text(GREEN_TEXT, optional_data) + ")") if optional_data is not None else "" + ": ")
            if empty_string(data):
                if optional_data is not None:
                    return optional_data
                else:
                    continue
            return data

    @staticmethod
    def synthesize_path(path: str):
        return path.replace("\\", "/")

    @staticmethod
    def open_with_notepad(file_path):
        Commander.execute(CommandStringGenerator.launch_notepad(file_path))

    @staticmethod
    def on_key_press():
        pass
