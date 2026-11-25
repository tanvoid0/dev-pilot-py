from sqlalchemy.orm import joinedload
from tabulate import tabulate

from py_helper.models.exception.app_exception import AppException
from py_helper.models.exception.missing_project_configuration_exception import MissingProjectConfigurationException
from py_helper.models.exception.resource_not_found_exception import ResourceNotFoundException
from py_helper.models.project_model import ProjectModel, ProjectType
from py_helper.processor.commander import Commander
from py_helper.processor.db_processor import DBProcessor
from py_helper.processor.file.file_processor import FileProcessor
from py_helper.processor.print_processor import color_text, RED_TEXT, BRED_TEXT, BGREEN_TEXT, GREEN_TEXT, WHITE_TEXT, \
    press_enter_to_continue, BYELLOW_TEXT
from py_helper.processor.util_processor import UtilProcessor
from py_helper.service.config_service import ConfigService
from py_helper.service.kubernetes.kubernetes_service import KubernetesService


class ProjectService:
    db = DBProcessor()
    config_service = ConfigService()
    kubernetes_service = KubernetesService()
    file_service = FileProcessor()
    projects: [ProjectModel] = []
    active_project: ProjectModel | None = None

    def __init__(self):
        self.find_active_project(safe_load=True)
        self.refresh_project_list()

    def find_active_project(self, safe_load=False) -> ProjectModel | None:
        config = self.config_service.get_config()
        try:
            session = self.db.get_session()
            project = session.query(ProjectModel).filter_by(id=config.project_id).options(
                joinedload(ProjectModel.deployment)).first()
            if project is None and not safe_load:
                raise MissingProjectConfigurationException()
            return project
        except ResourceNotFoundException as ex:
            if safe_load:
                return None
        return config.project

    def add_project(self):
        while True:
            project_path = self.file_service.reader.select_folder()
            # project_path: str = Commander.persistent_input("Enter Project Path")
            if self.file_service.file_exists(project_path):
                project = self.find_by_path(project_path)
                if project is None:
                    break
                else:
                    print(f"Invalid path. {color_text(RED_TEXT, 'It already exists.')}")
                    continue
            print(f"Invalid path. Does not exist: {project_path}")
        print(project_path)
        project_name = self.file_service.extract_sub_directory_from_path(project_path)
        project_name = Commander.persistent_input("Enter Project Name", project_name)
        project_type = ProjectType.get_type(project_path)
        print(project_type.value)
        ## FIXME: This is invalid code
        deployment = self.kubernetes_service.get_deployments_with_cloud_data(choice=True)

        new_project = ProjectModel(
            path=project_path,
            name=project_name,
            type=project_type.value,
            deployment_id=deployment
        )
        project_id = self.db.insert(new_project)
        self.update_project_path_config(project_id)

    def update_project_path_config(self, project_id):
        print("Updating active project:")
        project = self.find_by_id(project_id)
        self.config_service.update_project(project_id)
        print(
            f"Project '{color_text(BRED_TEXT, project.name)}' with path {color_text(BGREEN_TEXT, project.path)} has been set to active"
        )

    def find_by_id(self, _id: int) -> ProjectModel:
        return self.db.find_by_id(ProjectModel, _id)

    def find_by_path(self, path_name):
        session = self.db.get_session()
        project = session.query(ProjectModel).filter_by(path=path_name).first()
        return project

    def show_projects(self):
        data = []
        header_color = BYELLOW_TEXT
        index = 1
        self.refresh_project_list()
        self.refresh_active_project()
        for project in self.projects:
            if self.active_project is not None:
                if Commander.synthesize_path(project.path) == self.active_project.path:
                    data_color = BGREEN_TEXT
                elif not Commander.path_exist(project.path):
                    data_color = BRED_TEXT
                else:
                    data_color = WHITE_TEXT
            else:
                data_color = WHITE_TEXT
            data.append(
                (
                    color_text(data_color, index),
                    color_text(data_color, project.path),
                    color_text(data_color, project.name),
                    color_text(data_color, project.type),
                    color_text(data_color, '' if project.deployment is None else project.deployment.name),
                    color_text(data_color, '' if project.deployment is None else project.deployment.service_name),
                )
            )
            index += 1
        # Create a DataFrame from the list of dictionaries
        headers = [
            color_text(header_color, "Index"),
            color_text(header_color, "path"),
            color_text(header_color, "name"),
            color_text(header_color, "type"),
            color_text(header_color, "deployment_name"),
            color_text(header_color, "service_name"),
        ]

        # Print the DataFrame as a table
        table = tabulate(data, headers=headers, tablefmt="grid")
        print(table)

    def refresh_project_list(self):
        self.projects = self.db.get_session().query(ProjectModel).options(joinedload(ProjectModel.deployment)).all()
        return self.projects

    def refresh_active_project(self):
        self.active_project = self.find_active_project(safe_load=True)

    def show(self):
        print("Show projects")
        while True:
            try:
                print(f"Total Projects: {color_text(GREEN_TEXT, str(len(self.projects)))}")
                self.show_projects()

                print("s. Select Project")
                print("a. Add Project")
                # print("b. Update Project")
                print("r. Remove Project")
                print("0. Go back")
                choice, options = UtilProcessor.batch_picker()
                if choice == '0':
                    break
                elif choice == 's':
                    project = self.select_project(None if len(options) == 0 else options[0])
                    self.update_project_path_config(project.id)
                elif choice == 'a':
                    self.add_project()
                elif choice == 'u':
                    project = self.select_project(None if len(options) == 0 else options[0])
                    # self.update_project(project.id)
                elif choice == 'r':
                    project = self.select_project(None if len(options) == 0 else options[0])
                    self.remove_project(project.id)
                else:
                    print("Invalid choice...")
                    press_enter_to_continue()
            except AppException as ex:
                ex.print()
                press_enter_to_continue()

    def select_project(self, project_index: int = None):
        if len(self.projects) <= 0:
            print("No Project to make a selection")
            return None
        default_index = next((i for i, project in enumerate(self.projects) if project.id == self.active_project.id),
                             None)
        if project_index is None:
            project_index = input(
                f"Enter Project Index to select ({color_text(BRED_TEXT, 0)} to exit, default :{color_text(BRED_TEXT, '0' if self.active_project is None or default_index is None else default_index)}): "
            )
        if self.projects[int(project_index) - 1] == self.active_project.id:
            return None
        return self.projects[int(project_index) - 1]

    def update_project(self, project_id: int, project: ProjectModel):
        raise "Implementation required"

    def remove_project(self, project_id: int):
        self.db.remove(ProjectModel, project_id)
