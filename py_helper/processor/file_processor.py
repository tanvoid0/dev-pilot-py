import json
import os
import platform
import subprocess

import yaml

from py_helper.models.exception.exception_model import ExceptionModel


class FileProcessor:

    @staticmethod
    def current_path():
        return os.getcwd()

    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def read(file_path):
        try:
            with open(file_path, 'r') as file:
                return file
        except FileNotFoundError:
            print(f"File '{file_path} not found.")
        except json.JSONDecodeError as ex:
            print(f"Json decoding error: {str(ex)}")

    @staticmethod
    def read_json(file_path):
        try:
            with open(file_path, 'r') as json_file:
                json_string = json_file.read()
                return json.loads(json_string)

                # data = pd.read_json(json_file)
                # return data.to_dict()
        except FileNotFoundError:
            print(f"File '{file_path} not found.")
        except json.JSONDecodeError as ex:
            print(f"Json decoding error: {str(ex)}")

    @staticmethod
    def write_json(file_path, file):
        try:
            with open(file_path, 'w') as json_file:
                json_file.write(json.dumps(file, indent=2))
        except FileNotFoundError:
            print(f"File '{file_path} not found.")

    @staticmethod
    def save(file_name, file_data=""):
        with open(file_name, "w") as f:
            f.write(file_data)

    @staticmethod
    def remove(file_name):
        try:
            os.remove(file_name)
        except PermissionError as ex:
            raise ExceptionModel(f"Does not have enough permission to remove the file {file_name}.\nLog: {ex}")

    @staticmethod
    def copy_file(source_file, destination_file):
        try:
            subprocess.run(["copy", source_file, destination_file], shell=True)
        except Exception as ex:
            print("Error copying file")
            raise ex

    @staticmethod
    def write_yaml(file_name, data):
        with open(file_name, 'w') as file:
            yaml.dump(data, file)

    @staticmethod
    def read_text_file(file_name):
        # Windows
        if os.name == "nt":
            subprocess.call(["notepad.exe", file_name])
        # Linux or Mac
        elif os.name == "posix":
            subprocess.call(["gedit", file_name])
        else:
            raise ExceptionModel("Unsupported operation: {}".format(os.name))

    @staticmethod
    def get_platform():
        return platform.system()
