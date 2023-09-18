import re

from tabulate import tabulate

from py_helper.processor.print_processor import GREEN_TEXT, color_text, BGREEN_TEXT, BYELLOW_TEXT
from py_helper.processor.util_processor import UtilProcessor


class DeploymentModel:
    id: int
    name: str
    ready: str
    up_to_date: str
    available: str
    age: str
    stateful_set: bool
    selected: bool

    def __init__(self, id, name="", ready="", up_to_date=None, available=None, age=None, stateful_set=False,
                 selected=True):
        self.id = id
        self.name = name
        self.ready = ready
        self.stateful_set = stateful_set
        self.up_to_date = up_to_date
        self.available = available
        self.selected = selected
        if age is not None:
            self.age = UtilProcessor.round_days(int(age))

    def __repr__(self):
        return f"Deployment(id={self.id}, name={self.name}, ready={self.ready}, " \
               f"up_to_date={self.up_to_date}, available={self.available}, " \
               f"age={self.age}, stateful_set={self.stateful_set})"

    def ready_highlighter(self, string) -> str:
        if string == "0/1":
            return color_text(BYELLOW_TEXT, string)
        elif string == "1/1":
            return color_text(BGREEN_TEXT, string)
        else:
            return string

    @staticmethod
    def deployment_from_kubectl_command_string(string: str, namespace: str, show=False):
        pattern = r"(?P<name>\S+) +(?P<ready>\d+/\d+) +(?P<up_to_date>\d+) +(?P<available>\d+) +(?P<age>\d+)"
        deployments_tuples = re.findall(pattern, string)
        data = []
        for i in range(len(deployments_tuples)):
            data.append(
                DeploymentModel(
                    id=i + 1,
                    name=deployments_tuples[i][0],
                    ready=deployments_tuples[i][1],
                    up_to_date=deployments_tuples[i][2],
                    available=deployments_tuples[i][3],
                    age=deployments_tuples[i][4]
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
                    id=i + 1,
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
    def print_list(data, namespace):
        deployment_list = []
        for deployment in data:
            deployment_list.append(
                [deployment.id, deployment.name, deployment.ready, deployment.up_to_date, deployment.available,
                 deployment.age,
                 deployment.stateful_set,
                 deployment.selected
                 ])
        print(f"Deployments for namespace: {color_text(BGREEN_TEXT, namespace)}")
        headers = ["ID", "NAME", "READY", "UP-TO-DATE", "AVAILABLE", "AGE", "STATEFUL_SET", "SELECTED"]
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
