import os
from enum import Enum

from tabulate import tabulate
from sqlalchemy import String, inspect
from sqlalchemy.orm import Mapped, mapped_column

from py_helper.models.base_model import BaseModel
from py_helper.models.exception_model import ExceptionModel
from py_helper.models.runtime_var_model import RuntimeVarModel

# from py_helper.models.runtime_var_model import RuntimeVarModel
from py_helper.processor.commander import Commander
from py_helper.processor.db_processor import DBProcessor, get_session
from py_helper.processor.file_processor import FileProcessor
from py_helper.processor.print_processor import (
    RED_TEXT,
    color_text,
    GREEN_TEXT,
    BRED_TEXT,
    WHITE_TEXT,
    BGREEN_TEXT,
)


class ProjectType(Enum):
    MAVEN = "Maven"
    NPM = "Npm"
    FLUTTER = "Flutter"
    UNKNOWN = "Unknown"

    @staticmethod
    def get_type(project_path):
        file_exists = FileProcessor.file_exists

        if file_exists(os.path.join(project_path, "pom.xml")):
            return ProjectType.MAVEN
        elif file_exists(os.path.join(project_path, "package.json")):
            return ProjectType.NPM
        elif file_exists(os.path.join(project_path, "pubspec.yaml")):
            return ProjectType.FLUTTER
        else:
            return ProjectType.UNKNOWN

    @staticmethod
    def exec_func(project_type, maven=None, npm=None, flutter=None, unknown=None):
        if project_type == ProjectType.MAVEN.value:
            if maven is None:
                raise ExceptionModel("Maven Function Required")
            maven()
        elif project_type == ProjectType.NPM.value:
            if npm is None:
                raise ExceptionModel("npm Function Required")
            npm()
        elif project_type == ProjectType.FLUTTER.value:
            if flutter is None:
                raise ExceptionModel("flutter Function Required")
            flutter()
        elif project_type == ProjectType.UNKNOWN.value:
            if unknown is None:
                raise ExceptionModel("unknown Function Required")
            unknown()


class ProjectModel(BaseModel):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(500), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    docker_name: Mapped[str] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(255), default=ProjectType.UNKNOWN.value)
    deployment_name: Mapped[str] = mapped_column(String(255), nullable=True)
    service_name: Mapped[str] = mapped_column(String(255), nullable=True)

    @staticmethod
    def print_table(projects: []):
        data = []
        header_color = BRED_TEXT
        active_project = ProjectModel.find_active_project()
        for project in projects:
            if Commander.synthesize_path(project.path) == active_project.path:
                data_color = BGREEN_TEXT
            else:
                data_color = WHITE_TEXT
            data.append(
                (
                    color_text(data_color, project.id),
                    color_text(data_color, project.path),
                    color_text(data_color, project.name),
                    color_text(data_color, project.type),
                    color_text(data_color, project.docker_name),
                    color_text(data_color, project.deployment_name),
                    color_text(data_color, project.service_name),
                )
            )
        # Create a DataFrame from the list of dictionaries
        headers = [
            color_text(header_color, "id"),
            color_text(header_color, "path"),
            color_text(header_color, "name"),
            color_text(header_color, "type"),
            color_text(header_color, "docker_name"),
            color_text(header_color, "deployment_name"),
            color_text(header_color, "service_name"),
        ]

        # Print the DataFrame as a table
        table = tabulate(data, headers=headers, tablefmt="grid")
        print(table)

    @staticmethod
    def show():
        db = DBProcessor()
        print("Show projects")
        projects = db.get(ProjectModel)
        while True:
            try:
                print(f"Total Projects: {color_text(GREEN_TEXT, str(len(projects)))}")
                ProjectModel.print_table(projects)
                active_project = ProjectModel.find_active_project()
                project_id = input(
                    f"Enter Project id to select ({color_text(BRED_TEXT, 0)} to exit, default :{color_text(BRED_TEXT, active_project.id)}): "
                )
                if project_id == active_project.id or project_id == "0":
                    break
                ProjectModel.update_project_path_config(project_id)
                break
            except ExceptionModel as ex:
                ex.print()
                break

    @staticmethod
    def find_by_id(item_id=None):
        if item_id is None:
            ProjectModel.show()
            item_id = Commander.persistent_input("Select id: ")
            if item_id == 0:
                return
        db = DBProcessor()
        project = db.find_by_id(ProjectModel, item_id)
        if project is None:
            raise ExceptionModel(f"Project with id={item_id} not found")
        return project

    @staticmethod
    def find_by_path(path_name):
        session = get_session()
        project = session.query(ProjectModel).filter_by(path=path_name).first()
        return project

    @staticmethod
    def find_active_project():
        config = RuntimeVarModel.get()
        project = ProjectModel.find_by_path(config.active_project_path)
        if project is None:
            raise ExceptionModel(
                color_text(RED_TEXT, "Operation unsuccessful.") + " Add a project first"
            )
        project.docker_pre_tag = config.docker_pre_tag
        project.docker_post_tag = config.docker_post_tag
        project.path = Commander.synthesize_path(project.path)
        return project

    @staticmethod
    def insert():
        db = DBProcessor()
        while True:
            project_path = Commander.persistent_input("Enter Project Path")
            if FileProcessor.file_exists(project_path):
                project = ProjectModel.find_by_path(project_path)
                if project is None:
                    break
                else:
                    print(f"Invalid path. {color_text(RED_TEXT, 'It already exists.')}")
                    continue
            print(f"Invalid path. Does not exist: {project_path}")
        print(project_path)
        project_name = project_path.split("\\")[-1]
        project_name = project_name.split("/")[-1]
        project_name = Commander.persistent_input("Enter Project Name", project_name)
        docker_name = Commander.persistent_input(
            "Enter Docker Service Name", project_name
        )
        project_type = ProjectType.get_type(project_path)
        print(project_type.value)
        new_project = ProjectModel(
            path=project_path,
            name=project_name,
            docker_name=docker_name,
            type=project_type.value,
        )
        project_id = db.insert(new_project)
        ProjectModel.update_project_path_config(project_id)

    @staticmethod
    def update_project_path_config(project_id):
        print("Updating active project:")
        project = ProjectModel.find_by_id(project_id)
        RuntimeVarModel.update(
            active_project_path=project.path, active_project_type=project.type
        )
        print(
            f"Project '{color_text(BRED_TEXT, project.name)}' with path {color_text(BGREEN_TEXT, project.path)} has been set to active"
        )
