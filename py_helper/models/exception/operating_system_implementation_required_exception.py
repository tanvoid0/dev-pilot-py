import platform

from py_helper.models.exception.exception_model import ExceptionModel


class OperatingSystemImplementationRequiredException(ExceptionModel):
    def __init__(self, os):
        self.os = os
        if os is None:
            self.os = platform.system()

        super().__init__(f"Implementation required for OS: {self.os}")
