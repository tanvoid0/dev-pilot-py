from py_helper.models.exception.app_exception import AppException


class ConfigNotInitializedException(AppException):
    def __init__(self):
        super().__init__("Configuration data is not initialized yet.")
