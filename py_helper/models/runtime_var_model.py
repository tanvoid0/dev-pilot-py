import os
from typing import Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from py_helper.models.base_model import BaseModel
from py_helper.processor.db_processor import DBProcessor, get_session
from py_helper.processor.file_processor import FileProcessor
from py_helper.processor.print_processor import GREEN_TEXT, color_text

config_file = os.path.join(FileProcessor.current_path(), "config.json")


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
