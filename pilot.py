import subprocess
import sys
from enum import Enum

from py_helper.gui_app.kubernetes_app import KubernetesApp
from py_helper.models.project_model import ProjectType
from py_helper.processor.commander import Commander
from py_helper.processor.print_processor import color_text, BRED_TEXT
from py_helper.scripts.docker_script import DockerScript
from py_helper.scripts.kubernetes_script import KubernetesScript
from py_helper.scripts.maven_script import MavenScript
from py_helper.service.project_service import ProjectService

#
args = sys.argv

dictionary = {}
lists = []
# print(args)

# Iterate over the array
for item in args:
    # Split each item on the '=' character
    parts = item.split("=")

    # Check if it's in the 'key=value' format
    if len(parts) == 2:
        key, value = parts
        # Add it to the dictionary
        dictionary[key] = value
    elif item is not None and item != "":
        lists.append(item)

print(dictionary)

print(lists)


class AutoPilotSequence(Enum):
    PROJECT = "PROJECT"
    DOCKER = "DOCKER"
    KUBERNETES = "KUBERNETES"
    GIT = "GIT"
    REMOTE_GIT = "REMOTE_GIT"


def capture_output():
    output = subprocess.run(dictionary["exec"], capture_output=True)
    output = output.stdout.decode("utf-8")
    print("Output: {}".format(output))


if __name__ == "__main__":
    try:
        if "exec" in dictionary and dictionary['exec'] != '' and dictionary['exec'] is not None:
            dictionary['exec'] = dictionary['exec'][1:-1]  # Remove safety \' from args
            print(f"Running command: {dictionary['exec']}")
            Commander.execute(dictionary['exec'], show=True,
                              sync=True if 'sync' in lists else False)
            # output = subprocess.run(
            #     dictionary["exec"], shell=True
            # )  # capture_output=True, reads the output
        if "run" in dictionary and dictionary['run'] != '' and dictionary['run'] is not None:
            if dictionary['run'] == 'kubernetes':
                KubernetesApp()
                # KubernetesScript().cli_deployment_dashboard_view()
        if "pilot" in dictionary:
            print("Pilot dictionary")
            dictionary['pilot'] = dictionary['pilot'].split(",")

            # Notification.send("Pilot Engaged", dictionary['pilot'])
            commands = []

            if AutoPilotSequence.PROJECT.value in dictionary['pilot']:
                active_project = ProjectService().find_active_project()
                print(active_project.type)
                if active_project.type == ProjectType.MAVEN.value:
                    commands += MavenScript.auto_pilot()
            if AutoPilotSequence.DOCKER.value in dictionary['pilot']:
                commands += DockerScript.auto_pilot()
            if AutoPilotSequence.KUBERNETES.value in dictionary['pilot']:
                commands += KubernetesScript.auto_pilot()

            for command in commands:
                print(f"Running command: {color_text(BRED_TEXT, command)}")
                Commander.execute(command, sync=True)
    except Exception as ex:
        print(f"Exception Occurred: {ex}")
    input("Press Any key to continue")
# exit()
