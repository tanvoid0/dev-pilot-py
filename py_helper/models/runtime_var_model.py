import os
from typing import Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from py_helper.models.base_model import BaseModel
from py_helper.processor.db_processor import DBProcessor, get_session, get_db_engine
from py_helper.processor.file_processor import FileProcessor
from py_helper.processor.print_processor import GREEN_TEXT, color_text, RED_TEXT, YELLOW_TEXT

example_config_file = os.path.join(FileProcessor.current_path(), "config.json.example")
config_file = os.path.join(FileProcessor.current_path(), "config.json")
db_file = os.path.join(FileProcessor.current_path(), "db.sqlite")


class RuntimeVarModel(BaseModel):
    __tablename__ = "runtime_vars"

    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    docker_pre_tag: Mapped[str] = mapped_column(String(255), nullable=True)
    docker_post_tag: Mapped[str] = mapped_column(String(255), default="latest")
    active_project_path: Mapped[str] = mapped_column(String(500), nullable=True)
    active_project_type: Mapped[str] = mapped_column(String(255), default="Unknown")
    namespace: Mapped[Optional[str]]
    logo_view: Mapped[bool] = mapped_column(Boolean(), default=True)
    banner_path: Mapped[str] = mapped_column(String(500), default='robot')
    notification: Mapped[bool] = mapped_column(Boolean(), default=True)

    @staticmethod
    def first_setup() -> bool:
        try:
            if FileProcessor.file_exists(example_config_file):
                print("Example config file exists")
            if not FileProcessor.file_exists(config_file):
                # Create Config File
                FileProcessor.copy_file(example_config_file, config_file)

                config_data = FileProcessor.read_json(config_file)
                print(
                    f"Database Reset mode: {color_text(RED_TEXT, 'On') if config_data['db']['reset'] else color_text(GREEN_TEXT, 'Off')}")

                RuntimeVarModel.database_file_setup(config_data['db']['reset'])
                RuntimeVarModel.init()
                return True
            else:
                return False
        except Exception as ex:
            print(ex)

    @staticmethod
    def init():
        config_data = RuntimeVarModel.get_config_file()
        session = get_session()
        namespace = config_data['vars']['namespace']
        docker_pre_tag = config_data['vars']['docker-pre-tag']
        docker_post_tag = namespace if namespace is not None else "latest"
        runtime_var = RuntimeVarModel(docker_pre_tag=docker_pre_tag, docker_post_tag=docker_post_tag,
                                      namespace=namespace)
        session.add(runtime_var)
        session.commit()
        print("Runtime vars " + color_text(GREEN_TEXT, "configured..."))

    @staticmethod
    def get_config_file():
        file = FileProcessor.read_json(config_file)
        return file

    @staticmethod
    def set_config_file(file):
        FileProcessor.write_json(config_file, file)

    @staticmethod
    def get():
        db = DBProcessor()
        runtime_var = db.find_by_id(RuntimeVarModel, 1)
        return runtime_var

    @staticmethod
    def update(active_project_path=None, active_project_type=None):
        session = get_session()
        model = session.query(RuntimeVarModel).get(1)
        model.active_project_path = active_project_path
        model.active_project_type = active_project_type
        session.commit()
        return model

    @staticmethod
    def get_kubernetes_scale_config():
        config_file = RuntimeVarModel.get_config_file()
        return config_file['kubernetes']['scale']

    @staticmethod
    def database_file_setup(reset: bool):
        if reset:
            try:
                FileProcessor.remove(db_file)
            except:
                print("Database File doesn't exist")
        if not FileProcessor.file_exists(db_file):
            base_model = BaseModel
            FileProcessor.save(db_file)
            session = get_session()
            db_engine = get_db_engine()

            try:
                base_model.metadata.create_all(db_engine)
                print(color_text(YELLOW_TEXT, "Creating ") + "database")
                print("Database " + color_text(GREEN_TEXT, "created\n"))

                print(color_text(GREEN_TEXT, "Setting up") + " runtime vars")

                session.commit()

                # countdown_timer("Booting up Dev Pilot", config_data['vars']['startup-time'])
                print("System Booted...")
            except Exception as ex:
                print("Database Connection Failed {}".format(ex))
