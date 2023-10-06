import re

from tabulate import tabulate

from py_helper.processor.commander import Commander
from py_helper.processor.print_processor import color_text, BRED_TEXT, BGREEN_TEXT, BYELLOW_TEXT, clear_console
from py_helper.processor.util_processor import UtilProcessor


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
    def print_list(data, namespace):
        clear_console()
        deployment_list = []
        for deployment in data:
            deployment_list.append(
                [deployment.id,
                 DeploymentModel.ready_highlighter(deployment.ready, deployment.name),
                 DeploymentModel.ready_highlighter(deployment.ready),
                 deployment.up_to_date,
                 deployment.available,
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
