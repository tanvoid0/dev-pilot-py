import os

from py_helper.models.config_file_model import ConfigFileModel, KubernetesScaleConfigFileModel
from py_helper.models.file_type import FileType
from py_helper.processor.commander import Commander
from py_helper.processor.db_processor import DBProcessor
from py_helper.processor.file.file_processor import FileProcessor
from py_helper.processor.print_processor import color_text, RED_TEXT, GREEN_TEXT
from py_helper.utility.command_string_generator import CommandStringGenerator


class ConfigFileService:
    db = DBProcessor()
    file_processor = FileProcessor()
    example_config_file = os.path.join(FileProcessor.current_path(), "config.json.example")
    config_file = os.path.join(FileProcessor.current_path(), "config.json")
    db_file = os.path.join(FileProcessor.current_path(), "db.sqlite")
    kubernetes_config_files_dir = os.path.join(os.getcwd(), "local", "kube-configs")
    kubernetes_pod_log_files_dir = os.path.join(os.getcwd(), "local", "logs")

    def get_config_file(self) -> ConfigFileModel:
        return ConfigFileModel.from_json(self.file_processor.reader.read(self.config_file, file_type=FileType.JSON))

    def save_config_file(self, file: ConfigFileModel):
        self.file_processor.writer.write(file_path=self.config_file, file_data=file.to_json(), file_type=FileType.JSON)

    def get_kubernetes_scale_config(self) -> KubernetesScaleConfigFileModel:
        return self.get_config_file().kubernetes.scale

    def create_config_file_from_example_file(self) -> ConfigFileModel:
        if not self.file_processor.file_exists(self.config_file):
            config_file_data = ConfigFileModel()
            self.file_processor.writer.write(self.config_file, config_file_data.to_json(), file_type=FileType.JSON)
        else:
            config_file_data = self.file_processor.reader.read(self.config_file, file_type=FileType.JSON)
        return ConfigFileModel.from_json(config_file_data)

    def create_db_file_if_doesnt_exist(self, reset=False):
        print(
            f"Database Reset mode: {color_text(RED_TEXT, 'On') if reset else color_text(GREEN_TEXT, 'Off')}")
        if reset and self.file_processor.file_exists(self.db_file):
            self.file_processor.remove(self.db_file)
        if not self.file_processor.file_exists(self.db_file):
            self.file_processor.write(self.db_file, file_type=FileType.FILE)
            return True
        return False

    def database_file_setup(self, db_file, reset: bool) -> bool:
        if reset:
            self.file_processor.remove(db_file)
        if not self.file_processor.file_exists(db_file):
            self.file_processor.write(db_file)
            return False
        return True

    def remove_cached_file_configs_kubernetes(self):
        Commander.execute(
            CommandStringGenerator.remove_subdirectories(self.kubernetes_config_files_dir), show=True)

    def log_file_saver(self, file_path, data, view=True):
        file_name = f"{self.file_processor.extract_sub_directory_from_path(file_path)}.log"
        file_path = os.path.join(file_path, file_name)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_path = os.path.join(file_path, file_name)
        self.file_processor.writer.write(file_path, data, FileType.TEXT, file_name)
        if view:
            self.file_processor.reader.read(file_path, with_notepad=True)
