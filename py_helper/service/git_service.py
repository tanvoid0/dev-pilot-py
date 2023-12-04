import re

from py_helper.processor.commander import Commander
from py_helper.processor.print_processor import color_text, BLUE_TEXT
from py_helper.service.config_service import ConfigService
from py_helper.service.project_service import ProjectService
from py_helper.service.string_generator.git_command_string_generator import GitCommandStringGenerator


class GitService:
    git_string_generator = GitCommandStringGenerator()
    config_service = ConfigService()
    project_service = ProjectService()

    def status(self):
        active_project = self.project_service.find_active_project()
        Commander.execute(self.git_string_generator.status(active_project.path), show=True)

    def checkout_branch(self):
        active_project = self.project_service.find_active_project()
        branch_name = Commander.persistent_input("Enter branch name")
        Commander.execute(self.git_string_generator.switch_branch(active_project.path, branch_name), show=True)

    def remote_link_generate(self):
        active_project = self.project_service.find_active_project()
        output = Commander.execute(GitCommandStringGenerator.get_remote(active_project.path))
        match = re.search(r"git@(.*?):(.*?)/(.*?)\.git", output)
        if match:
            output = "https://" + match.group(1) + "/" + match.group(2) + "/" + match.group(3)
            print(f"Remote link: {color_text(BLUE_TEXT, output)}")
            print(f"Pipeline link: {color_text(BLUE_TEXT, output + '/pipelines/results/page/1')}")

            branch_name = Commander.execute(GitCommandStringGenerator.status(active_project.path))
            pattern = r'On branch (\S+)'
            match = re.search(pattern, branch_name)

            if match:
                branch_name = match.group(1)
                print(f"PR Link: {color_text(BLUE_TEXT, output + f'/branch/{branch_name}')}")
            # Commander.print_url(output)
        else:
            print("No remote url found")
            return None
        input("press enter to continue")
