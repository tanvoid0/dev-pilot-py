import os
from datetime import datetime

import yaml

from py_helper.models.kube_model import DeploymentModel
from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.models.project_model import ProjectModel
from py_helper.models.runtime_var_model import RuntimeVarModel
from py_helper.processor.commander import Commander
from py_helper.processor.file_processor import FileProcessor


class KubernetesScript(OptionGroupModel):
    def __init__(self):
        super().__init__(
            "Kubernetes Commands",
            [
                OptionModel(
                    "kdg", "Get Deployments", "Find deployments", self.get_deployments
                ),
                OptionModel("ksu", "Upscale in batch", "", self.scale_batch),
                OptionModel(
                    "ksd", "Downscale in batch", "", lambda: self.scale_batch(down=True)
                ),
                OptionModel("kpx", "Run Proxy", "", None),
                OptionModel("kpf", "Run Port forward", "", None),
                OptionModel("kpr", "Run Port forward for Remote Debug", "", None),
                OptionModel(
                    "kcg",
                    "Get Kubernetes Deployment config",
                    "",
                    self.get_yaml_deployment_config,
                ),
                OptionModel(
                    "ksg",
                    "Get Kubernetes Service config",
                    "",
                    self.get_yaml_service_config,
                ),
            ],
        )

    def get_deployments(self):
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
            RuntimeVarModel.set_config_file(config_file)

        ordered_data = DeploymentModel.order_by_selection_names(
            data, updated_deployments
        )
        DeploymentModel.print_list(ordered_data, config.namespace)

        return ordered_data

    def scale_batch(self, down=False):
        config_file = RuntimeVarModel.get_config_file()
        config = RuntimeVarModel.get()
        deployments = self.get_deployments()
        cmd = []
        for deployment in deployments:
            if deployment.selected:
                cmd.append(
                    f"kubectl scale -n {config.namespace} {'statefulset' if deployment.stateful_set else 'deployment'} {deployment.name} --replicas={'0' if down else '1'};"
                )
        delay = (
            config_file["kubernetes"]["scale"]["down"]
            if down
            else config_file["kubernetes"]["scale"]["up"]
        )
        batch_cmd = f" sleep {delay}s; ".join(cmd)
        Commander.execute_externally(batch_cmd)

    def get_yaml_deployment_config(self):
        # kubectl get deployment test-deployment -o yaml
        config = RuntimeVarModel.get()
        active_project = ProjectModel.find_active_project()
        deployment_name = active_project.deployment_name
        yaml_config = Commander.execute(
            f"kubectl get deployment {deployment_name} -o yaml -n {config.namespace}",
            show=True,
        )
        yaml_config = yaml.safe_load(yaml_config)
        ## Copy Values

        # Image name
        print(yaml_config["spec"]["template"]["spec"]["containers"][0]["image"])

        # JAVA_TOOL_OPTIONS
        env = yaml_config["spec"]["template"]["spec"]["containers"][0]["env"]
        env_exists = False
        for env_item in env:
            if env_item["name"] == "JAVA_TOOL_OPTIONS":
                env_exists = True
                break

        print(env_exists)

        now = datetime.now()
        file_name = f"{deployment_name}-config-{now:%Y-%m-%d-%H-%M-%S}.yaml"
        file_path = os.path.join(
            FileProcessor.current_path(), "kube-configs", deployment_name
        )
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        FileProcessor.write_yaml(os.path.join(file_path, file_name), yaml_config)

    def get_yaml_service_config(self):
        # kubectl get deployment test-deployment -o yaml
        config = RuntimeVarModel.get()
        active_project = ProjectModel.find_active_project()
        service_name = active_project.service_name
        yaml_config = Commander.execute(
            f"kubectl get service {service_name} -o yaml -n {config.namespace}",
            show=True,
        )
        yaml_config = yaml.safe_load(yaml_config)
        ## Copy Values
        print(yaml_config["spec"]["ports"])
        env = yaml_config["spec"]["ports"]
        env_exists = False
        for env_item in env:
            if env_item["name"] == "debug":
                env_exists = True
                break
        print(env_exists)

        now = datetime.now()
        file_name = f"{service_name}-config-{now:%Y-%m-%d-%H-%M-%S}.yaml"
        file_path = os.path.join(
            FileProcessor.current_path(), "kube-configs", service_name
        )
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_path = os.path.join(file_path, file_name)
        FileProcessor.write_yaml(file_path, yaml_config)
        FileProcessor.read_text_file(file_path)
