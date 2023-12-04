from typing import Optional

from sqlalchemy import String, Boolean, Integer, Text, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from py_helper.models.base_model import BaseModel
from py_helper.models.project_model import ProjectModel


class ConfigModel(BaseModel):
    __tablename__ = "config"

    id: Mapped[int] = Column(Integer, primary_key=True, default=1)

    ### Project ########
    # active_project_path: Mapped[str] = Column(String(500), nullable=True)
    # active_project_type: Mapped[str] = Column(String(255), default="Unknown")
    project_id: Mapped[int] = Column(Integer, ForeignKey('projects.id'), nullable=True)
    project: Mapped[ProjectModel] = relationship('ProjectModel')

    ### Utility #########
    # logo_view: Mapped[bool] = Column(Boolean(), default=True)
    # banner_path: Mapped[str] = Column(String(500), default='robot')
    notification: Mapped[bool] = Column(Boolean(), default=True)

    ### Kubernetes properties ######
    namespace: Mapped[Optional[str]]
    docker_pre_tag: Mapped[str] = Column(String(255), nullable=True)
    docker_post_tag: Mapped[str] = Column(String(255), default="latest")
    kubernetes_ip: Mapped[Optional[str]] = Column(Text(1000), nullable=True)
    kubernetes_token: Mapped[Optional[str]]
    scale_up_timeout: Mapped[str] = Column(Integer(), nullable=False)
    scale_down_timeout: Mapped[str] = Column(Integer(), nullable=False)

    ### VPN ####
    vpn_username: Mapped[Optional[str]]
    vpn_password: Mapped[Optional[str]]
    vpn_config: Mapped[Optional[str]]

    def get_docker_image_for_active_project(self):
        return f"{f'{self.docker_pre_tag}/' if self.docker_pre_tag is None or self.docker_pre_tag else ''}{self.project.name}:{self.docker_post_tag}"
