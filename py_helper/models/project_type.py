import os
from enum import Enum

from py_helper.models.exception.app_exception import AppException
from py_helper.processor.file.file_processor import FileProcessor


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
                raise AppException("Maven Function Required")
            maven()
        elif project_type == ProjectType.NPM.value:
            if npm is None:
                raise AppException("npm Function Required")
            npm()
        elif project_type == ProjectType.FLUTTER.value:
            if flutter is None:
                raise AppException("flutter Function Required")
            flutter()
        elif project_type == ProjectType.UNKNOWN.value:
            if unknown is None:
                raise AppException("unknown Function Required")
            unknown()
