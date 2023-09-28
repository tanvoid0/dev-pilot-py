import os
import subprocess

import pandas as pd
from tabulate import tabulate

from py_helper.processor.file_processor import FileProcessor
from py_helper.processor.print_processor import color_text, GREEN_TEXT


def empty_string(data):
    return data is None or data.strip() == ""


class Commander:
    @staticmethod
    def execute(commands, show=False):
        process = subprocess.run(commands, capture_output=True, shell=True)
        output = process.stdout.decode("utf-8")
        if show:
            print(output)
        return output

    @staticmethod
    def execute_externally(command_to_run, python=False):
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
    def execute_shell(command):
        pltform = FileProcessor.get_platform()
        if pltform == "Linux":
            subprocess.Popen(
                ["gnome-terminal", "--", os.path.join(os.getcwd(), "exec.sh"), command],
                cwd=os.getcwd(),
            )
        else:
            raise "OS Not supported"

    @staticmethod
    def execute_python(args=None, execute=""):
        print(os.getcwd())
        pltfrm = FileProcessor.get_platform()
        if args is None:
            args = []
        if pltfrm == "Windows":
            subprocess.Popen(
                ["start", "cmd", "/k", "python", "pilot.py", f"exec={execute}"] + args,
                shell=True,
            )
        elif pltfrm == "Linux":
            subprocess.Popen(
                ["gnome-terminal", "--", "python3", "pilot.py", f"exec='{execute}'"] + args,
                cwd=os.getcwd(),
            )
            # subprocess.Popen(
            #     ["gnome-terminal", "-e", "python3", "pilot.py", f"exec={execute}"] + args,
            #     cwd=os.getcwd(),
            # )
            # subprocess.Popen(["python", "pilot.py"])
        else:
            raise "OS Not supported"

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
                     " (" + (color_text(GREEN_TEXT, optional_data) + ")")
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
