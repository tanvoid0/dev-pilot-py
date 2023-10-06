from py_helper.models.exception.exception_model import ExceptionModel


class ImplementationRequiredException(ExceptionModel):
    def __init__(self):
        super("Implementation Required for this function")

    @staticmethod
    def ex():
        raise ImplementationRequiredException()
