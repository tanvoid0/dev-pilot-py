from py_helper.models.exception.app_exception import AppException
from py_helper.models.project_model import ProjectType
from py_helper.processor.commander import Commander
from py_helper.processor.print_processor import (
    color_text,
    BRED_TEXT,
    BLUE_TEXT,
    BWHITE_TEXT,
    clear_console,
    press_enter_to_continue, BCYAN_TEXT, )
from py_helper.scripts.docker_script import DockerScript
from py_helper.scripts.flutter_script import FlutterScript
from py_helper.scripts.git_script import GitScript
from py_helper.scripts.internet_script import InternetScript
from py_helper.scripts.kubernetes_script import KubernetesScript
from py_helper.scripts.maven_script import MavenScript
from py_helper.scripts.npm_script import NpmScript
from py_helper.scripts.project_script import ProjectScript
from py_helper.scripts.secret_scripts import secret_scripts
from py_helper.scripts.utility_script import UtilityScript
from py_helper.service.config_service import ConfigService
from py_helper.service.project_service import ProjectService


class DashboardProcessor:
    scripts = []
    output = ""
    commands = {}
    last_choice = ""
    config_service = ConfigService()
    project_service = ProjectService()

    def reinitialize_scripts(self):
        self.scripts.clear()
        self.output = ""
        self.commands = {}
        self.add_initial_scripts()
        self.add_conditional_scripts()

    def add_initial_scripts(self):
        self.scripts.append(InternetScript())
        self.scripts.append(UtilityScript())
        self.scripts.append(KubernetesScript())
        self.scripts.append(ProjectScript())
        for secret_script in secret_scripts():
            self.scripts.append(secret_script)

    def add_conditional_scripts(self):
        try:
            active_project = self.project_service.find_active_project()
            self.scripts.append(DockerScript())
            self.scripts.append(GitScript())

            ProjectType.exec_func(
                project_type=None if active_project is None else active_project.type,
                maven=lambda: self.scripts.append(MavenScript()),
                npm=lambda: self.scripts.append(NpmScript()),
                flutter=lambda: self.scripts.append(FlutterScript())
            )
        except AppException as ex:
            pass

    def process_script(self, script):
        self.output += script.print_option(self.last_choice)
        self.copy_commands(script.commands)

    def run(self):
        while True:
            self.reinitialize_scripts()
            for script in self.scripts:
                self.process_script(script)
            self.print_options()
            self.print_configs()
            self.pick_options()
            clear_console()

    def pick_options(self):
        Commander.on_key_press()
        self.last_choice = Commander.persistent_input("Pick an option")
        Commander.on_key_press()
        self.run_option(self.last_choice)
        clear_console()

    def copy_commands(self, commands):
        for value in commands:
            if value.choice in self.commands:
                raise AppException(
                    f'Duplicate keys found. Remove Duplicate option keys \'{value.choice}\' from scripts.')
            self.commands[value.choice] = value

    def run_option(self, option):
        if option == "x":
            exit(0)
        try:
            for key, value in self.commands.items():
                if key == option:
                    value.method()
                    return
            print("No option found")
        except AppException as ex:
            ex.print()
            raise ex
        except Exception as ex:
            print("Some exception occurred")
            print(ex)
            raise ex
        finally:
            press_enter_to_continue()

    def print_options(self):
        print("Dev Pilot")

        print(self.output)

    def print_configs(self):
        config = self.config_service.get_config()
        color = BCYAN_TEXT
        print(f"{color_text(color, 'Namespace           : ')}{config.namespace}")
        print(f"{color_text(color, 'Docker Pre Tag      : ')}{config.docker_pre_tag}")
        if config.project is not None:
            # active_project = self.project_service.find_active_project()
            print(
                f"{color_text(color, 'Deployment Image    : ')}{config.get_docker_image_for_active_project()}")
            print(f"{color_text(color, 'Active Project Name : ')}{config.project.name}")
            print(f"{color_text(color, 'Active Project Path : ')}{config.project.path}")
            print(f"{color_text(color, 'Active Project Type : ')}{config.project.type}")

    def print_option_item(self, option, feature, command):
        print(
            f"{color_text(BRED_TEXT, option)}. {color_text(BWHITE_TEXT, feature)} {color_text(BLUE_TEXT, command)}"
        )
