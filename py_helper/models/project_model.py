from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_helper.models.base_model import BaseModel
from py_helper.models.kube_model import KubernetesDeploymentModel
from py_helper.models.project_type import ProjectType


# from py_helper.models.runtime_var_model import RuntimeVarModel


class ProjectModel(BaseModel):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(500), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255), default=ProjectType.UNKNOWN.value)
    deployment_id: Mapped[int] = Column(Integer, ForeignKey('deployments.id'), nullable=True)
    deployment: Mapped[KubernetesDeploymentModel] = relationship('KubernetesDeploymentModel', back_populates='project')
