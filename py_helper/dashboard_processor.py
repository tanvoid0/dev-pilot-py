from py_helper.models.exception_model import ExceptionModel
from py_helper.models.project_model import ProjectModel, ProjectType
from py_helper.processor.commander import Commander
from py_helper.processor.print_processor import (
    color_text,
    BRED_TEXT,
    BLUE_TEXT,
    BWHITE_TEXT,
    clear_console,
    press_enter_to_continue,
)
from py_helper.scripts.docker_script import DockerScript
from py_helper.scripts.git_script import GitScript
from py_helper.scripts.internet_script import InternetScript
from py_helper.scripts.kubernetes_script import KubernetesScript
from py_helper.scripts.maven_script import MavenScript
from py_helper.scripts.npm_script import NpmScript
from py_helper.scripts.project_script import ProjectScript
from py_helper.scripts.utility_script import UtilityScript


class DashboardProcessor:
    scripts = []
    output = ""
    commands = {}
    last_choice = ""

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

    def add_conditional_scripts(self):
        try:
            active_project = ProjectModel.find_active_project()
            self.scripts.append(DockerScript())
            self.scripts.append(GitScript())

            ProjectType.exec_func(
                project_type=active_project.type,
                maven=lambda: self.scripts.append(MavenScript()),
                npm=lambda: self.scripts.append(NpmScript()),
            )
        except ExceptionModel as ex:
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
            self.pick_options()
            clear_console()

    def pick_options(self):
        self.last_choice = Commander.persistent_input("Pick an option")
        self.run_option(self.last_choice)
        clear_console()

    def copy_commands(self, commands):
        for value in commands:
            self.commands[value.choice] = value

    def run_option(self, option):
        if option == "x":
            exit(0)

        for key, value in self.commands.items():
            if key == option:
                value.method()
                press_enter_to_continue()
                return
        print("No option found")

    def print_options(self):
        print("Dev Pilot")

        print(self.output)

    def print_option_item(self, option, feature, command):
        print(
            f"{color_text(BRED_TEXT, option)}. {color_text(BWHITE_TEXT, feature)} {color_text(BLUE_TEXT, command)}"
        )
