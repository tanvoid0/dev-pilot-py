from py_helper.models.exception.app_exception import AppException


class ImplementationRequiredAppException(AppException):
    def __init__(self):
        super("Implementation Required for this function")

    @staticmethod
    def ex():
        raise ImplementationRequiredAppException()
