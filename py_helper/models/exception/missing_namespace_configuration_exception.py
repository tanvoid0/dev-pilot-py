from py_helper.models.exception.app_exception import AppException


class MissingNamespaceConfigurationException(AppException):
    def __init__(self):
        super().__init__("Namespace needs to be set first")
