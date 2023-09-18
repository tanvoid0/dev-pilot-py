import os
import subprocess

import pandas as pd
from tabulate import tabulate

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
        execute_script_file_path = os.path.join(os.path.abspath(os.getcwd()), 'exec.sh')
        # python_command = ""
        # if FileProcessor.check_platform("Linux"):
        #     python_command = "python3"
        # else:
        #     python_command = "python"
        # process = subprocess.Popen(['python', execute_script_file_path], stdout=subprocess.PIPE, text=True)
        # return_code = process.wait()
        #
        # stdout, stderr = process.communicate()

        if python:
          command_to_run = f"python exec.py -k {command_to_run}"
        # subprocess.Popen([execute_script_file_path, command_to_run], shell=True)
        output = subprocess.run([execute_script_file_path, command_to_run], shell=True,  stdout=subprocess.PIPE, text=True)
        # print("Executing Command {}".format(command_to_run))
        # subprocess.Popen(['x-terminal-emulator', '-e', 'bash', '-c', 'exec.sh', 'echo "Hello from shell script"'])

        # output = subprocess.Popen(['x-terminal-emulator', '-e', 'bash', 'exec.sh', command_to_run], shell=True,
        #                           stdout=subprocess.PIPE, text=True)
        print("Finished")
        # print(output.stdout)

    @staticmethod
    def print(commands):
        print(Commander.execute(commands))

    @staticmethod
    def print_table(data):
        df = pd.DataFrame(data)
        table = tabulate(df, headers='keys', tablefmt='pretty')
        print(table)

    @staticmethod
    def persistent_input(query, optional_data=None):
        query += (" (" + (color_text(GREEN_TEXT, optional_data) + ")") if optional_data is not None else "") + ": "
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
    def execute_python(args=[], exec=""):
        subprocess.Popen(["start", "cmd", "/k", "python", "pilot.py", f"exec={exec}"] + args, shell=True)
