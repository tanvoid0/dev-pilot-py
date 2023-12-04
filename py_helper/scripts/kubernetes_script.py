import os
from datetime import datetime

import yaml

from py_helper.models.exception.app_exception import AppException
from py_helper.models.file_type import FileType
from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.processor.commander import Commander
from py_helper.processor.file.file_processor import FileProcessor
from py_helper.processor.print_processor import press_enter_to_continue, clear_console
from py_helper.processor.util_processor import UtilProcessor
from py_helper.service.config_service import ConfigService
from py_helper.service.kubernetes.kubernetes_service import KubernetesService
from py_helper.service.project_service import ProjectService
from py_helper.service.string_generator.kubernetes_command_string_generator import KubernetesCommandStringGenerator
from py_helper.utility.command_string_generator import CommandStringGenerator
from py_helper.utility.validator import Validator


class KubernetesScript(OptionGroupModel):
    config_service = ConfigService()
    config_file_service = config_service.config_file_service
    kubernetes_service = KubernetesService()
    project_service = ProjectService()
    file_processor = FileProcessor()

    def __init__(self):
        config = self.config_service.get_config()
        namespace = "" if config is None or config.namespace is None else config.namespace
        current_docker_image = self.config_service.get_current_docker_image()

        super().__init__(
            "Kubernetes Commands",
            [
                OptionModel("kd", "Open Kubernetes Dashboard", "", self.open_kubernetes_dashboard),
                OptionModel(
                    "kg", "CLI Kubernetes Dashboard", "", self.cli_deployment_dashboard_view,
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
                    lambda: self.get_yaml_deployment_config(save=True, view=True),
                ),
                OptionModel(
                    "ksc",
                    "Get Kubernetes Service Config",
                    "",
                    self.get_service_config,
                ),
                OptionModel(
                    "kcn",
                    "Change Namespace",
                    f"Current Namespace: {namespace}",
                    self.change_namespace,
                ),
                OptionModel(
                    "ktc",
                    "Toggle Custom/Latest Image",
                    f"current image: {current_docker_image}",
                    self.kubernetes_service.toggle_custom_image,
                )
                # OptionModel(
                #     "ksg",
                #     "Get Kubernetes Service config",
                #     "",
                #     self.get_yaml_service_config,
                # ),
            ],
        )

    def auto_pilot(self):
        config = self.config_service.get_config()
        scale_config = self.config_file_service.get_kubernetes_scale_config()
        project = self.project_service.find_active_project()
        return [
            KubernetesCommandStringGenerator.scale(config.namespace, project.name, False, True),
            f"sleep {scale_config.down}",
            KubernetesCommandStringGenerator.scale(config.namespace, project.name, False, False),
        ]

    def open_kubernetes_dashboard(self):
        config = self.config_service.get_config()
        Commander.open_url(
            f"http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/pod?namespace={config.namespace}")

    @staticmethod
    def open_kubernetes_cli_dashboard():
        Commander.execute_python(args=['run=kubernetes'])

    def change_namespace(self):
        config = self.config_service.get_config()
        namespace = self.kubernetes_service.select_namespace()
        if namespace != config.namespace:
            config.namespace = namespace
            self.config_service.update_namespace(namespace=namespace)

    def run_proxy(self):
        Commander.execute_shell("kubectl proxy")

    def port_forward(self):
        config = self.config_service.get_config()
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(
            f"kubectl -n {config.namespace} port-forward svc/{active_project.deployment.service_name} 7000:80")

    def port_forward_remote(self):
        config = self.config_service.get_config()
        active_project = self.project_service.find_active_project()
        Commander.execute_shell(
            f"kubectl -n {config.namespace} port-forward svc/{active_project.deployment.service_name} 7001:81")

    def cli_deployment_dashboard_view(self):
        config = self.config_service.get_config()
        active_project = self.project_service.find_active_project()
        # deployments = self.kubernetes_service.get_deployments_with_cloud_data()
        self.kubernetes_service.cli_deployments_init()
        while True:
            clear_console()
            self.kubernetes_service.print_deployments(self.kubernetes_service.deployments, config.namespace)
            print("\nx. Go back to main menu")
            print("0. Refresh data")
            print("1. Upscale a service")
            print("2. Downscale a service")
            print("3. Restart a service")
            # print("4. Log Active deployment")
            # print("5. Toggle selection")
            data = Commander.persistent_input("Enter choice")
            if data == "x":
                break
            elif data == "0":
                print("Refreshing deployment list")
                self.kubernetes_service.cli_deployments_init()
                continue
            elif data == "1":
                print("Upscaling service")
                deployment = self.kubernetes_service.deployment_picker()
                if deployment is None:
                    press_enter_to_continue()
                    continue
                self.kubernetes_service.scale_service.scale_deployment(deployment.name,
                                                                       stateful_set=deployment.stateful_set)
            elif data == "2":
                print("Downscaling service")
                deployment = self.kubernetes_service.deployment_picker()
                if deployment is None:
                    press_enter_to_continue()
                    continue
                self.scale_deployment(deployment.name, down=True, stateful_set=deployment.stateful_set)
            elif data == "3":
                print("Restarting service")
                deployment = self.kubernetes_service.deployment_picker()
                if deployment is None:
                    press_enter_to_continue()
                    continue
                self.restart_deployment(deployment.name,
                                        stateful_set=deployment.stateful_set)

            # elif data == "4":
            #     print(f"Logging deployment logs for {config.namespace}.{active_project.deployment_name}")
            #     KubernetesScript.log_deployment(config.namespace, active_project.deployment_name)

        #     elif data == "sdfasdf":
        #         print("Reordering deployment")
        #         deployment_id1 = int(Commander.persistent_input("Enter id of the deployment from the table"))
        #         deployment_id2 = int(Commander.persistent_input("Enter id of the deployment from the table"))
        #         if (deployment_id1 > len(deployments) or deployment_id1 < 1) or (
        #                 deployment_id2 > len(deployments) or deployment_id2 < 1):
        #             print("Invalid id")
        #             press_enter_to_continue()
        #             continue
        #         print(deployments[deployment_id1 - 1])
        #         print(deployments[deployment_id2 - 1])
        #         self.swap_deployment_order(deployment_id1 - 1,
        #                                    deployment_id2 - 1)
        #         deployments = self.get_deployments()
        #
        #     else:
        #         print("Invalid choice")
        #     press_enter_to_continue()

    @staticmethod
    def log_deployment(namespace, deployment_name, save=True):
        log_text = Commander.execute(
            f"kubectl logs deployment/{deployment_name} -n {namespace}",
            show=False,
        )

        if save:
            # TODO: Fix
            # KubernetesScript.log_file_saver(deployment_name, log_text)
            pass
        return log_text

    def swap_deployment_order(self, item1, item2):
        pass
        # TODO: Fix
        # config_file = self.config_service.get_config_file()
        # deployments = config_file.kubernetes['kubernetes']['deployments']
        # new_d = {}
        # object1 = {}
        # object2 = {}
        # for i, (key, value) in enumerate(deployments.items()):
        #     if i == item1:
        #         object2 = {key: value}
        #     elif i == item2:
        #         object1 = {key: value}
        #
        # for i, (key, value) in enumerate(deployments.items()):
        #     if i == item1:
        #         new_d
        #
        # config_file['kubernetes']['deployments'] = new_d
        # RuntimeVarModel.set_config_file(config_file)

    def restart_deployment(self, deployment=None, namespace=None, stateful_set=False):
        config_file = self.config_service.get_config_file()
        down_time = config_file.kubernetes.scale.down

        if deployment is None:
            project = self.project_service.find_active_project()
            deployment = project.deployment.name
        if namespace is None:
            config = self.config_service.get_config()
            namespace = config.namespace

        # Downscale
        cmd = "clear;"
        cmd += CommandStringGenerator.kubernetes_scale(namespace, deployment, True, stateful_set)
        cmd += UtilProcessor.count_down_timer_shell_string(f"Scaling up {deployment} in ", down_time)
        cmd += CommandStringGenerator.kubernetes_scale(namespace, deployment, False, stateful_set)
        Commander.execute_shell(cmd)

    def get_deployments(self, reset_cache=False):
        pass
        # TODO: Fix
        # config = self.config_service.get_config()
        #
        # output = Commander.execute(f"kubectl get statefulsets -n {config.namespace}")
        # data = DeploymentModel.statefulset_from_kubectl_command_string(
        #     output, config.namespace
        # )
        # output = Commander.execute(f"kubectl get deployments -n {config.namespace}")
        # data += DeploymentModel.deployment_from_kubectl_command_string(
        #     output, config.namespace
        # )
        #
        # config_file = self.config_service.get_config_file()
        # deployments = DeploymentModel.get_name_selection_map_from_list(data)
        # updated_deployments = config_file["kubernetes"]["deployments"]
        # if len(config_file["kubernetes"]["deployments"]) == 0:
        #     updated_deployments = DeploymentModel.get_name_selection_map_from_list(data)
        # else:
        #     for key, value in deployments.items():
        #         if key not in updated_deployments:
        #             updated_deployments = value
        # if len(updated_deployments) != config_file["kubernetes"]["deployments"]:
        #     config_file['kubernetes']['deployments'] = updated_deployments
        #     if reset_cache:
        #         ConfigModel.set_config_file(config_file)
        #
        # ordered_data = DeploymentModel.order_by_selection_names(
        #     data,
        #     updated_deployments
        # )
        #
        # return ordered_data

    def scale_deployment(self, deployment_name, down=False, stateful_set=False):
        config = self.config_service.get_config()
        Commander.execute_shell(
            CommandStringGenerator.kubernetes_scale(config.namespace, deployment_name, down, stateful_set))

    def scale_batch(self, down=False):
        config_file = self.config_service.get_config_file()
        config = self.config_service.get_config()
        deployments = self.kubernetes_service.get_deployments_from_db()
        delay = (
            config_file.kubernetes.scale.down
            if down
            else config_file.kubernetes.scale.up
        )
        cmd = [f"clear; "]
        first_item = True
        for item in deployments:
            if item.selected:
                if first_item:
                    cmd.append(
                        f"echo \"Scaling {'Down' if down else 'Up'} {item.name} of {config.namespace} namespace\";")
                    first_item = False
                else:
                    cmd.append(UtilProcessor.count_down_timer_shell_string(
                        f"Scaling {'Down' if down else 'Up'} {item.name} of {config.namespace} namespace in ", delay))
                cmd.append(
                    f"kubectl scale -n {config.namespace} {'statefulset' if item.stateful_set else 'deployment'} {item.name} --replicas={'0' if down else '1'};"
                )

        # batch_cmd = f" sleep {delay}s; ".join(cmd)
        batch_cmd = "".join(cmd)
        Commander.execute_shell(batch_cmd)

    def get_yaml_deployment_config(self, deployment_name=None, namespace=None, save=False, view=False):
        # kubectl get deployment test-deployment -o yaml
        if deployment_name is None:
            active_project = self.project_service.find_active_project()
            if active_project.deployment is None or active_project.deployment.name is None:
                print("Project Not Linked to a deployment")
                raise "Project is not linked to a deployment"
            deployment_name = active_project.deployment.name
        if namespace is None:
            config = self.config_service.get_config()
            namespace = config.namespace
        # deployment = self.kubernetes_service.get_deployment(deployment_name, namespace)
        # deployment_spec = deployment.spec
        # deployment_yaml = yaml.safe_dump(deployment_spec)
        # print(deployment_yaml)
        yaml_config = Commander.execute(
            f"kubectl get deployment {deployment_name} -o yaml -n {namespace}",
            show=False,
        )
        yaml_config = yaml.safe_load(yaml_config)
        if save:
            self.save_file(deployment_name, 'deployment', namespace, yaml_config, view=True)
        return yaml_config

    def get_service_config(self):
        namespace = self.config_service.get_config().namespace
        service_name = Commander.persistent_input("Kubernetes Service Name")
        KubernetesScript.get_yaml_service_config(service_name, namespace, save=False, view=True)

    def get_yaml_service_config(self, service_name, namespace, save=False, view=False):
        # kubectl get deployment test-deployment -o yaml
        if service_name is None or service_name == "":
            raise "Service Name Required"
        yaml_config = Commander.execute(
            f"kubectl get service {service_name} -o yaml -n {namespace}",
            show=False,
        )
        yaml_config = yaml.safe_load(yaml_config)
        if save:
            self.save_file(service_name, 'service', namespace, yaml_config, view=True)
        return yaml_config

    def get_yaml_config_map(self, config_name, namespace, save=False, view=False):
        if namespace is None or config_name is None:
            raise AppException("Namespace and/or namespace is required for operation")
        yaml_config = Commander.execute(f"kubectl get configmap {config_name} -o yaml -n {namespace}", show=True)
        yaml_config = yaml.safe_load(yaml_config)
        if save:
            self.save_file(config_name, 'config', namespace, yaml_config, view=True)
        return yaml_config

    def get_yaml_secret_config(self, secret_name, namespace, save=False, view=False):
        Validator.required_validator([{'secret_name': secret_name}, {'namespace': namespace}])
        yaml_config = Commander.execute(f"kubectl get secret {secret_name} -o yaml -n {namespace}", show=False)
        yaml_config = yaml.safe_load(yaml_config)
        if save:
            self.save_file(secret_name, 'secret', namespace, yaml_config, view=True)
        return yaml_config

    def save_file(self, item_name, item_type, namespace, data, view=False):
        now = datetime.now()
        file_name = f"{item_name}-{now:%Y-%m-%d-%H-%M-%S}.yaml"
        file_path = os.path.join(
            self.file_processor.current_path(), "local", "kube-configs", namespace, item_type, item_name
        )
        os.makedirs(file_path, exist_ok=True)
        file_path = os.path.join(file_path, file_name)
        self.file_processor.writer.write(file_path, data, file_type=FileType.YAML)
        if view:
            self.file_processor.reader.read(file_path, with_notepad=True)
