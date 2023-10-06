from py_helper.models.exception.exception_model import ExceptionModel


class InputRequiredException(ExceptionModel):
    def __init__(self, data):
        self.fields = data
        super().__init__(f"Inputs required for {data}")

