import re
from typing import Dict

from kubernetes.client import V1DeploymentCondition, V1Deployment, V1DeploymentStatus
from sqlalchemy import String, Column, Integer, Boolean
from sqlalchemy.orm import relationship, Mapped
from tabulate import tabulate

from py_helper.models.base_model import BaseModel
from py_helper.processor.commander import Commander
from py_helper.processor.db_processor import DBProcessor
from py_helper.processor.print_processor import color_text, BRED_TEXT, BGREEN_TEXT, BYELLOW_TEXT, clear_console
from py_helper.processor.util_processor import UtilProcessor


class KubernetesDeploymentReplicaSet:
    replicas: int = None
    ready_replicas: int = None
    available_replicas: int = None
    unavailable_replicas: int = None
    updated_replicase: int = None
    conditions: [V1DeploymentCondition] = []

    def __init__(self, status: V1DeploymentStatus):
        self.replicas = status.replicas
        self.ready_replicas = status.ready_replicas
        self.available_replicas = status.available_replicas
        self.unavailable_replicas = status.unavailable_replicas
        self.updated_replicase = status.updated_replicas
        self.conditions = status.conditions


class KubernetesDeploymentModel(BaseModel):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    service_name = Column(String(255), nullable=True)
    stateful_set: Mapped[bool] = Column(Boolean, default=False)
    order_seq: Mapped[int] = Column(Integer, default=0)
    selected: Mapped[bool] = Column(Boolean, default=True)
    project = relationship('ProjectModel', back_populates='deployment', uselist=False)

    ## Additional properties
    timestamp = None  # items.metadata.creationTimestamp
    labels = {}  # items.metadata.labels
    # items.status.replicas
    # items.status.updatedReplicas
    # items.status.readyReplicas
    # items.status.availableReplicas
    # items.status.conditions [] => type, status, lastUpdateTime, lastTransitionTime, reason, message
    # replicas: Mapped[KubernetesDeploymentReplicaSet] = None
    # items.status.conditions [] => one of the array has type=Progressing, status=True, reason=NewReplicaSetAvailable, message="ReplicaSet \"app-deployment-5dcd13a44x\" has successfully progressed."
    pod = None
    status = None
    data = None

    def set_properties_from_kubernetes(self, deployment: V1Deployment):
        if deployment is None:
            return
        self.timestamp = deployment.metadata.creation_timestamp
        self.labels = deployment.metadata.labels
        self.status = deployment.status
        # self.replicas = KubernetesDeploymentReplicaSet(deployment.status)
        self.pod = KubernetesDeploymentModel.extract_pod_from_deployment(deployment.status.conditions)

    @staticmethod
    def extract_pod_from_deployment(objects: [V1DeploymentCondition]):
        """Finds the deployment name from the given objects.

          Args:
            objects: A list of objects.

          Returns:
            The deployment name, or None if not found.
            """
        if objects is None:
            return
        for obj in objects:
            if obj.type == 'Progressing' and obj.status == 'True':
                match = re.search(r"ReplicaSet \"(.*?)\" has successfully progressed.", obj.message)
                if match:
                    return match.group(1)
        return None

    @staticmethod
    def swap_order(id1, id2):
        print(f"Id1{id1} id2: {id2}")
        db = DBProcessor()
        db.swap_order(KubernetesDeploymentModel, id1=id1, id2=id2)
        return db.get(KubernetesDeploymentModel)


class PodModel:
    id: int
    name: str
    ready: str
    status: str
    restarts: str
    age: str
    deployment_name: str

    def __init__(self, _id, name="", ready="", status=None, restarts=None, age=None, stateful_set=False,
                 selected=True):
        self.id = _id
        self.name = name
        self.ready = ready
        self.stateful_set = stateful_set
        self.status = status
        self.restarts = restarts
        self.selected = selected
        self.age = age
        # if age is not None:
        #     self.age = UtilProcessor.round_days(int(age))

    @staticmethod
    def pod_from_kubectl(namespace: str, deployment_name):
        output = Commander.execute(f"kubectl get pods -n {namespace} | grep \"{deployment_name}.*\"")
        # print(output)

        return []

    @staticmethod
    def find_pod_by_deployment_name(pods: [], deployment_name: str):
        filtered_pods = []
        for item in pods:
            if item.name.startswith(deployment_name):
                filtered_pods.append(item)
        return filtered_pods


class DeploymentModel:
    id: int
    name: str
    ready: str
    up_to_date: str
    available: str
    age: str
    stateful_set: bool
    selected: bool
    pods: []

    def __init__(self, _id, name="", ready="", up_to_date=None, available=None, age=None, stateful_set=False,
                 selected=True, pods=[]):
        self.id = _id
        self.name = name
        self.ready = ready
        self.stateful_set = stateful_set
        self.up_to_date = up_to_date
        self.available = available
        self.selected = selected
        if age is not None:
            self.age = UtilProcessor.round_days(int(age))
        self.pods = pods

    def __repr__(self):
        return f"Deployment(id={self.id}, name={self.name}, ready={self.ready}, " \
               f"up_to_date={self.up_to_date}, available={self.available}, " \
               f"age={self.age}, stateful_set={self.stateful_set})"

    @staticmethod
    def ready_highlighter(string, value=None) -> str:
        if string == "0/1":
            return color_text(BYELLOW_TEXT, f"Scaling - {string}" if value is None else value)
        elif string == "1/1":
            return color_text(BGREEN_TEXT, f"Ready   - {string}" if value is None else value)
        elif string == "0/0":
            return color_text(BRED_TEXT, "Inactive" if value is None else value)
        else:
            return string

    @staticmethod
    def deployment_from_kubectl_command_string(string: str, namespace: str, show=False):
        pattern = r"(?P<name>\S+) +(?P<ready>\d+/\d+) +(?P<up_to_date>\d+) +(?P<available>\d+) +(?P<age>\d+)"
        deployments_tuples = re.findall(pattern, string)
        data = []
        for i in range(len(deployments_tuples)):
            # pods = PodModel.pod_from_kubectl(namespace, deployments_tuples[i][0])
            data.append(
                DeploymentModel(
                    _id=i + 1,
                    name=deployments_tuples[i][0],
                    ready=deployments_tuples[i][1],
                    up_to_date=deployments_tuples[i][2],
                    available=deployments_tuples[i][3],
                    age=deployments_tuples[i][4],
                    # pods=PodModel.find_pod_by_deployment_name(pods, deployments_tuples[i][0])
                )
            )

        if show:
            DeploymentModel.print_list(data, namespace)
        return data

    def statefulset_from_kubectl_command_string(string: str, namespace: str, show=False):
        pattern = r"(?P<name>\S+) +(?P<ready>\d+/\d+) +(?P<age>\d+)"
        deployments_tuples = re.findall(pattern, string)
        data = []
        for i in range(len(deployments_tuples)):
            data.append(
                DeploymentModel(
                    _id=i + 1,
                    name=deployments_tuples[i][0],
                    ready=deployments_tuples[i][1],
                    age=deployments_tuples[i][2],
                    stateful_set=True,
                )
            )
        if show:
            DeploymentModel.print_list(data, namespace)
        return data

    @staticmethod
    def print_list(data: Dict[str, KubernetesDeploymentModel], namespace):
        clear_console()
        deployment_list = []
        i = 1
        for key, deployment in data.items():
            deployment_list.append(
                [
                    i,
                    key,
                    # DeploymentModel.ready_highlighter(deployment.data.ready_replicas),
                    # deployment.id,
                    # DeploymentModel.ready_highlighter(deployment.ready, deployment.name),
                    # DeploymentModel.ready_highlighter(deployment.ready),
                    # deployment.up_to_date,
                    # deployment.available,
                    # deployment.age,
                    deployment.stateful_set,
                    deployment.selected
                ])
            i += 1
        print(f"Deployments for namespace: {color_text(BGREEN_TEXT, namespace)}")
        headers = [
            "ID",
            "NAME",
            # "READY",
            # "UP-TO-DATE",
            # "AVAILABLE",
            # "AGE",
            "STATEFUL_SET",
            "SELECTED"]
        print(tabulate(deployment_list, headers=headers))

    @staticmethod
    def get_name_selection_map_from_list(data):
        deployment_list = {}
        for deployment in data:
            deployment_list[deployment.name] = deployment.selected
        return deployment_list

    @staticmethod
    def order_by_selection_names(data, order):
        ordered_data = []
        _id = 1
        for name, selection in order.items():
            for deployment in data:
                if deployment.name == name:
                    deployment.id = _id
                    deployment.selected = selection
                    ordered_data.append(deployment)
                    _id += 1
                    break
        return ordered_data
