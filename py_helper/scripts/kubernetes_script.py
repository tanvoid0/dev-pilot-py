import os
from datetime import datetime

import yaml

from py_helper.models.exception.exception_model import ExceptionModel
from py_helper.models.kube_model import DeploymentModel
from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.models.runtime_var_model import RuntimeVarModel
from py_helper.processor.commander import Commander
from py_helper.processor.file_processor import FileProcessor
from py_helper.processor.print_processor import press_enter_to_continue
from py_helper.processor.util_processor import UtilProcessor
from py_helper.scripts.string_generator.kubernetes_command_string_generator import KubernetesCommandStringGenerator
from py_helper.utility.command_string_generator import CommandStringGenerator
from py_helper.utility.validator import Validator


class KubernetesScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Kubernetes Commands",
            [
                OptionModel(
                    "kdg", "Get Deployments", "Find deployments", self.show_deployments
                ),
                OptionModel('ksr', "Restart deployment", "", self.restart_deployment),
                OptionModel("ksu", "Upscale in batch", "", self.scale_batch),
                OptionModel(
                    "ksd", "Downscale in batch", "", lambda: self.scale_batch(down=True)
                ),
                OptionModel("kpx", "Run Proxy", "", self.run_proxy),
                OptionModel("kpf", "Run Port forward", "", self.port_forward),
                OptionModel("kpr", "Run Port forward for Remote Debug", "", self.port_forward_remote),
                OptionModel(
                    "kcg",
                    "Get Kubernetes Deployment config",
                    "",
                    self.get_yaml_deployment_config,
                ),
                OptionModel(
                    "ksc",
                    "Get Kubernetes Service Config",
                    "",
                    self.get_service_config,
                ),
                OptionModel(
                    "kcd",
                    "Delete Kubernetes Cached Config",
                    "",
                    self.remove_cached_configs
                )
                # OptionModel(
                #     "ksg",
                #     "Get Kubernetes Service config",
                #     "",
                #     self.get_yaml_service_config,
                # ),
            ],
        )

    @staticmethod
    def auto_pilot():
        config = RuntimeVarModel.get()
        scale_config = RuntimeVarModel.get_kubernetes_scale_config()
        project = ProjectModel.find_active_project()
        return [
            KubernetesCommandStringGenerator.scale(config.namespace, project.deployment_name, False, True),
            f"sleep {scale_config['down']}",
            KubernetesCommandStringGenerator.scale(config.namespace, project.deployment_name, False, False),
        ]

    @staticmethod
    def run_proxy():
        Commander.execute_shell("kubectl proxy")

    @staticmethod
    def port_forward():
        config = RuntimeVarModel.get()
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(f"kubectl -n {config.namespace} port-forward svc/{active_project.service_name} 7000:80")

    @staticmethod
    def port_forward_remote():
        config = RuntimeVarModel.get()
        active_project = ProjectModel.find_active_project()
        Commander.execute_shell(f"kubectl -n {config.namespace} port-forward svc/{active_project.service_name} 7001:81")

    @staticmethod
    def show_deployments():
        config = RuntimeVarModel.get()
        active_project = ProjectModel.find_active_project()
        deployments = KubernetesScript.get_deployments(reset_cache=True)
        while True:
            DeploymentModel.print_list(deployments, config.namespace)
            print("\nx. Go back to main menu")
            print("0. Refresh data")
            print("1. Upscale a service")
            print("2. Downscale a service")
            print("3. Restart a service")
            print("4. Log Active deployment")
            print("5. Toggle selection")
            data = Commander.persistent_input("Enter choice")
            if data == "x":
                break
            elif data == "0":
                print("Refreshing deployment list")
                deployments = KubernetesScript.get_deployments()
                continue
            elif data == "1":
                print("Upscaling service")
                deployment_id = int(Commander.persistent_input("Enter id of the deployment from the table"))
                if deployment_id > len(deployments) or deployment_id <= 0:
                    print("Invalid id.")
                    press_enter_to_continue()
                    continue
                KubernetesScript.scale_deployment(deployments[deployment_id - 1].name, stateful_set=deployments[
                    deployment_id - 1].stateful_set)
            elif data == "2":
                print("Downscaling service")
                deployment_id = int(Commander.persistent_input("Enter id of the deployment from the table"))
                if deployment_id > len(deployments) or deployment_id <= 0:
                    print("Invalid id.")
                    press_enter_to_continue()
                    continue
                KubernetesScript.scale_deployment(deployments[deployment_id - 1].name, down=True,
                                                  stateful_set=deployments[deployment_id - 1].stateful_set)
            elif data == "3":
                print("Restarting service")
                deployment_id = int(Commander.persistent_input("Enter id of the deployment from the table"))
                if deployment_id > len(deployments) or deployment_id <= 0:
                    print("Invalid id.")
                    press_enter_to_continue()
                    continue
                KubernetesScript.restart_deployment(deployments[deployment_id - 1].name,
                                                    stateful_set=deployments[deployment_id - 1].stateful_set)

            elif data == "4":
                print(f"Logging deployment logs for {config.namespace}.{active_project.deployment_name}")
                KubernetesScript.log_deployment(config.namespace, active_project.deployment_name)

            elif data == "sdfasdf":
                print("Reordering deployment")
                deployment_id1 = int(Commander.persistent_input("Enter id of the deployment from the table"))
                deployment_id2 = int(Commander.persistent_input("Enter id of the deployment from the table"))
                if (deployment_id1 > len(deployments) or deployment_id1 < 1) or (
                        deployment_id2 > len(deployments) or deployment_id2 < 1):
                    print("Invalid id")
                    press_enter_to_continue()
                    continue
                print(deployments[deployment_id1 - 1])
                print(deployments[deployment_id2 - 1])
                KubernetesScript.swap_deployment_order(deployment_id1 - 1,
                                                       deployment_id2 - 1)
                deployments = KubernetesScript.get_deployments()

            else:
                print("Invalid choice")
            press_enter_to_continue()

    @staticmethod
    def log_deployment(namespace, deployment_name, save=True):
        log_text = Commander.execute(
            f"kubectl logs deployment/{deployment_name} -n {namespace}",
            show=False,
        )

        if save:
            KubernetesScript.log_file_saver(deployment_name, log_text)
        return log_text

    @staticmethod
    def swap_deployment_order(item1, item2):
        config_file = RuntimeVarModel.get_config_file()
        deployments = config_file['kubernetes']['deployments']
        new_d = {}
        object1 = {}
        object2 = {}
        for i, (key, value) in enumerate(deployments.items()):
            if i == item1:
                object2 = {key: value}
            elif i == item2:
                object1 = {key: value}

        for i, (key, value) in enumerate(deployments.items()):
            if i == item1:
                new_d

        config_file['kubernetes']['deployments'] = new_d
        # RuntimeVarModel.set_config_file(config_file)

    @staticmethod
    def restart_deployment(deployment=None, namespace=None, stateful_set=False):
        config_file = RuntimeVarModel.get_config_file()
        down_time = config_file["kubernetes"]["scale"]["down"]

        if deployment is None:
            project = ProjectModel.find_active_project()
            deployment = project.deployment_name
        if namespace is None:
            config = RuntimeVarModel.get()
            namespace = config.namespace

        # Downscale
        cmd = "clear;"
        cmd += CommandStringGenerator.kubernetes_scale(namespace, deployment, True, stateful_set)
        cmd += UtilProcessor.count_down_timer_shell_string(f"Scaling up {deployment} in ", down_time)
        cmd += CommandStringGenerator.kubernetes_scale(namespace, deployment, False, stateful_set)
        Commander.execute_shell(cmd)

    @staticmethod
    def get_deployments(reset_cache=False):
        config = RuntimeVarModel.get()

        output = Commander.execute(f"kubectl get statefulsets -n {config.namespace}")
        data = DeploymentModel.statefulset_from_kubectl_command_string(
            output, config.namespace
        )
        output = Commander.execute(f"kubectl get deployments -n {config.namespace}")
        data += DeploymentModel.deployment_from_kubectl_command_string(
            output, config.namespace
        )

        config_file = RuntimeVarModel.get_config_file()
        deployments = DeploymentModel.get_name_selection_map_from_list(data)
        updated_deployments = config_file["kubernetes"]["deployments"]
        if len(config_file["kubernetes"]["deployments"]) == 0:
            updated_deployments = DeploymentModel.get_name_selection_map_from_list(data)
        else:
            for key, value in deployments.items():
                if key not in updated_deployments:
                    updated_deployments = value
        if len(updated_deployments) != config_file["kubernetes"]["deployments"]:
            config_file['kubernetes']['deployments'] = updated_deployments
            if reset_cache:
                RuntimeVarModel.set_config_file(config_file)

        ordered_data = DeploymentModel.order_by_selection_names(
            data,
            updated_deployments
        )

        return ordered_data

    @staticmethod
    def scale_deployment(deployment_name, down=False, stateful_set=False):
        config = RuntimeVarModel.get()
        Commander.execute_shell(
            CommandStringGenerator.kubernetes_scale(config.namespace, deployment_name, down, stateful_set))

    def scale_batch(self, down=False):
        config_file = RuntimeVarModel.get_config_file()
        config = RuntimeVarModel.get()
        deployments = self.get_deployments()
        delay = (
            config_file["kubernetes"]["scale"]["down"]
            if down
            else config_file["kubernetes"]["scale"]["up"]
        )
        cmd = ["clear;"]
        for i in range(len(deployments)):
            if deployments[i].selected:
                if i != 0:
                    cmd.append(UtilProcessor.count_down_timer_shell_string(
                        f"Scaling {'Down' if down else 'Up'} {deployments[i].name} in ", delay))
                cmd.append(
                    f"kubectl scale -n {config.namespace} {'statefulset' if deployments[i].stateful_set else 'deployment'} {deployments[i].name} --replicas={'0' if down else '1'};"
                )

        # batch_cmd = f" sleep {delay}s; ".join(cmd)
        batch_cmd = "".join(cmd)
        Commander.execute_shell(batch_cmd)

    @staticmethod
    def get_yaml_deployment_config(deployment_name=None, namespace=None, save=False, view=False):
        # kubectl get deployment test-deployment -o yaml
        if deployment_name is None:
            active_project = ProjectModel.find_active_project()
            deployment_name = active_project.deployment_name
        if namespace is None:
            config = RuntimeVarModel.get()
            namespace = config.namespace
        yaml_config = Commander.execute(
            f"kubectl get deployment {deployment_name} -o yaml -n {namespace}",
            show=False,
        )
        yaml_config = yaml.safe_load(yaml_config)
        if save:
            KubernetesScript.yaml_file_saver(deployment_name, yaml_config, view=view)
        return yaml_config

    @staticmethod
    def get_service_config():
        namespace = RuntimeVarModel.get().namespace
        service_name = Commander.persistent_input("Kubernetes Service Name")
        KubernetesScript.get_yaml_service_config(service_name, namespace, save=False, view=True)

    @staticmethod
    def get_yaml_service_config(service_name, namespace, save=False, view=False):
        # kubectl get deployment test-deployment -o yaml
        if service_name is None or service_name == "":
            raise "Service Name Required"
        yaml_config = Commander.execute(
            f"kubectl get service {service_name} -o yaml -n {namespace}",
            show=False,
        )
        yaml_config = yaml.safe_load(yaml_config)
        if save:
            KubernetesScript.yaml_file_saver(service_name, yaml_config, view=view)
        return yaml_config

    @staticmethod
    def get_yaml_config_map(config_name, namespace, save=False, view=False):
        if namespace is None or config_name is None:
            raise ExceptionModel("Namespace and/or namespace is required for operation")
        yaml_config = Commander.execute(f"kubectl get configmap {config_name} -o yaml -n {namespace}", show=True)
        yaml_config = yaml.safe_load(yaml_config)
        if save:
            KubernetesScript.yaml_file_saver(config_name, yaml_config, view=view)
        return yaml_config

    @staticmethod
    def get_yaml_secret_config(secret_name, namespace, save=False, view=False):
        Validator.required_validator([{'secret_name': secret_name}, {'namespace': namespace}])
        yaml_config = Commander.execute(f"kubectl get secret {secret_name} -o yaml -n {namespace}", show=False)
        yaml_config = yaml.safe_load(yaml_config)
        if save:
            KubernetesScript.yaml_file_saver(secret_name, yaml_config, view=view)
        return yaml_config

    @staticmethod
    def yaml_file_saver(service_name, yaml_data, view=True):
        now = datetime.now()
        file_name = f"{service_name}-{now:%Y-%m-%d-%H-%M-%S}.yaml"
        file_path = os.path.join(
            FileProcessor.current_path(), "local", "kube-configs", service_name
        )
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_path = os.path.join(file_path, file_name)
        FileProcessor.write_yaml(file_path, yaml_data)
        if view:
            Commander.open_with_notepad(file_path)
        return file_path

    @staticmethod
    def log_file_saver(name, data, view=True):
        file_name = f"{name}.log"
        file_path = os.path.join(FileProcessor.current_path(), "local", "logs", name)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_path = os.path.join(file_path, file_name)
        FileProcessor.save(file_path, data)
        if view:
            Commander.open_with_notepad(file_path)

    @staticmethod
    def remove_cached_configs():
        Commander.execute(
            CommandStringGenerator.remove_subdirectories(os.path.join(os.getcwd(), "local", "kube-configs")), show=True)
