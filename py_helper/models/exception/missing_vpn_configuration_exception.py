from py_helper.models.exception.app_exception import AppException


class MissingVPNConfigurationException(AppException):
    def __init__(self):
        super().__init__("VPN configuration in config.json file needs to be set first")