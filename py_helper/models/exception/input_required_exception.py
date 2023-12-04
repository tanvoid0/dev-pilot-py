from py_helper.models.exception.app_exception import AppException


class InputRequiredAppException(AppException):
    def __init__(self, data):
        self.fields = data
        super().__init__(f"Inputs required for {data}")
