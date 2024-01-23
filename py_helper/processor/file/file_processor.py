import os

from py_helper.models.exception.app_exception import AppException
from py_helper.models.file_type import FileType
from py_helper.processor.file.file_formatter import FileFormatter
from py_helper.processor.file.file_reader_processor import FileReaderProcessor
from py_helper.processor.file.file_writer_processor import FileWriterProcessor


class FileProcessor:
    reader: FileReaderProcessor = FileReaderProcessor()
    writer: FileWriterProcessor = FileWriterProcessor()
    formatter: FileFormatter = FileFormatter()

    def read(self, file_path, file_type):
        self.reader.read(file_path, file_type)

    def write(self, file_path, file_data=None, file_type=FileType.FILE):
        self.writer.write(file_path, file_data, file_type)

    @staticmethod
    def extract_sub_directory_from_path(file_path):
        return file_path.split("\\")[-1].split("/")[-1]

    @staticmethod
    def current_path():
        return os.getcwd()

    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)

    """
    Create Files/Folders
    """

    ################################################################

    @staticmethod
    def remove(file_name):
        try:
            os.remove(file_name)
        except PermissionError as ex:
            raise AppException(f"Does not have enough permission to remove the file {file_name}.\nLog: {ex}")
    #
    # @staticmethod
    # def copy_file(source_file, destination_file):
    #     try:
    #         OSCommander.run(
    #             linux= lambda: subprocess.run(["copy", source_file, destination_file], shell=True)
    #         )
    #     except Exception as ex:
    #         print("Error copying file")
    #         raise ex
