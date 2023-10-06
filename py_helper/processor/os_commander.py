import platform

from py_helper.models.exception.operating_system_implementation_required_exception import \
    OperatingSystemImplementationRequiredException


class OSCommander:
    os = platform.system()

    @staticmethod
    def run(windows=None, linux=None, mac=None, common=None):
        if common is not None:
            return common()
        elif OSCommander.os == "Windows":
            if windows is None:
                raise OperatingSystemImplementationRequiredException(OSCommander.os)
            return windows()
        elif OSCommander.os == "Linux":
            if linux is None:
                raise OperatingSystemImplementationRequiredException(OSCommander.os)
            return linux()
        elif OSCommander.os == "Mac":
            if linux is None:
                raise OperatingSystemImplementationRequiredException(OSCommander.os)
            return mac()
        else:
            raise OperatingSystemImplementationRequiredException(OSCommander.os)
