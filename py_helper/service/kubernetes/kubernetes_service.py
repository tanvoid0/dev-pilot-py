from typing import Dict

from tabulate import tabulate

from py_helper.client.kubernetes_client import KubernetesClient
from py_helper.client.kubernetes_watcher_client import KubernetesWatcherClient
from py_helper.models.exception.missing_namespace_configuration_exception import MissingNamespaceConfigurationException
from py_helper.models.exception.resource_not_found_exception import ResourceNotFoundException
from py_helper.models.kube_model import KubernetesDeploymentModel
from py_helper.processor.commander import Commander
from py_helper.processor.db_processor import get_session, DBProcessor
from py_helper.processor.file.file_processor import FileProcessor
from py_helper.processor.print_processor import color_text, BGREEN_TEXT, RED_TEXT, GREEN_TEXT, YELLOW_TEXT
from py_helper.service.config_service import ConfigService
from py_helper.service.kubernetes.kubernetes_scale_service import KubernetesScaleService
from py_helper.service.string_generator.kubernetes_command_string_generator import KubernetesCommandStringGenerator


class KubernetesService:
    client = KubernetesClient()
    watcher_client = KubernetesWatcherClient()
    scale_service = KubernetesScaleService()
    config_service = ConfigService()
    file_processor = FileProcessor()
    db = DBProcessor()

    deployments: {str: KubernetesDeploymentModel} = {}

    def cli_deployments_init(self):
        self.deployments = self.get_deployments_with_cloud_data()

    ### Warning: Using order instead of id to make them ordered as well as pickable
    def deployment_picker(self):
        deployment_order = int(Commander.persistent_input("Enter id of the deployment from the table"))
        for item in self.deployments:
            if deployment_order == self.deployments[item].order_seq:
                return self.deployments[item]
        print("Invalid id.")
        return None

    ########## Model Based services ###########################################
    def add_resources(self, item, statefulset=False):
        session = get_session()
        service_name = None
        if item.metadata.labels is not None and 'app.kubernetes.io/name' in item.metadata.labels:
            service_name = item.metadata.labels['app.kubernetes.io/name']
        new_model = KubernetesDeploymentModel(
            name=item.metadata.name,
            stateful_set=statefulset,
            service_name=service_name,
            order_seq=self.db.next_order_seq_for_table(KubernetesDeploymentModel)
        )
        session.add(new_model)
        session.commit()
        session.refresh(new_model)
        return new_model

    ###########################################################################

    """
    Logger
    """

    def log_pod(self):
        pass

    @staticmethod
    def get_token():
        return Commander.execute(KubernetesCommandStringGenerator.get_token()).replace('\n', '')

    def toggle_selection(self, deployment_name):
        session = self.db.get_session()
        deployment = session.query(KubernetesDeploymentModel).filter_by(name=deployment_name).first()
        if deployment is None:
            raise ResourceNotFoundException('Deployment', 'name', deployment_name)
        deployment.selected = not deployment.selected
        session.commit()
        return deployment

    def toggle_custom_image(self):
        config = self.config_service.get_config()
        active_project = config.project
        print(
            f"{color_text(RED_TEXT, 'Previous image:')} {config.get_docker_image_for_active_project()}")
        config_file = self.config_service.get_config_file()
        if config.docker_post_tag == 'latest':
            docker_pre_tag = config_file.kubernetes.docker_pre_tag
            docker_post_tag = config.namespace
        else:
            docker_pre_tag = config_file.kubernetes.docker_pre_tag_latest
            docker_post_tag = 'latest'
        config.docker_pre_tag = docker_pre_tag
        config.docker_post_tag = docker_post_tag
        print(
            f"{color_text(GREEN_TEXT, 'New Image:')} {config.get_docker_image_for_active_project()}")
        print(
            f"{color_text(YELLOW_TEXT, 'Warning:')} make sure the custom image is set to deployment's config file. Also, for your own custom pre_tag, set the config data in config.json file. Take a look at vars.docker_pre_tag and vars.docker_post_tag")
        self.config_service.toggle_docker_tag(docker_pre_tag, docker_post_tag)

    def select_namespace(self):
        namespace_list = self.client.get_namespaces()
        if len(namespace_list) <= 0:
            return None
        for i in range(len(namespace_list)):
            print(f"{i}. {namespace_list[i]}")
        namespace_choice = Commander.persistent_input("Enter default namespace title", namespace_list[0])
        if namespace_choice not in namespace_list:
            print("Invalid choice")
            self.select_namespace()
        return namespace_choice

    def get_deployment(self, deployment_name: str, namespace: str):
        return self.client.get_deployment(deployment_name, namespace)

    def get_deployments_from_db(self) -> [KubernetesDeploymentModel]:
        session = get_session()
        return session.query(KubernetesDeploymentModel).order_by(KubernetesDeploymentModel.order_seq).all()

    def get_deployments_with_cloud_data(self, show=False, choice=False) -> Dict[str, KubernetesDeploymentModel]:
        config = self.config_service.get_config()
        namespace = config.namespace
        deployments_from_db = self.get_deployments_from_db()
        deployments_map = {}
        deployments_map_with_live_data = {}

        # Something resets the selected in this loop
        for item in deployments_from_db:
            deployments_map[item.name] = item

        stateful_sets, deployments = self.client.fetch_deployments_and_stateful_sets_ordered(namespace)

        for item in stateful_sets.items:
            if item.metadata.name not in deployments_map:
                deployments_map[item.metadata.name] = self.add_resources(item, statefulset=True)
            deployments_map[item.metadata.name].set_properties_from_kubernetes(item)

        for deployment in deployments.items:
            if deployment.metadata.name not in deployments_map:
                deployments_map[deployment.metadata.name] = self.add_resources(deployment)
            deployments_map[deployment.metadata.name].set_properties_from_kubernetes(deployment)

        for item in deployments_map:
            if deployments_map[item].timestamp is not None:
                deployments_map_with_live_data[deployments_map[item].name] = deployments_map[item]

        if show or choice:
            self.print_deployments(deployments_map_with_live_data, namespace)
        if choice:
            return self.pick_deployment(deployments_map_with_live_data)

        return deployments_map_with_live_data

    def pick_deployment(self, deployments_map):
        while True:
            choice = Commander.persistent_input("Enter deployment name (Enter 0 to leave empty)")
            if choice is not None and choice != "":
                if choice == "0":
                    return None
                if choice in deployments_map:
                    return deployments_map[choice].id
                else:
                    print("Invalid Deployment name. Try again...")

    def print_deployments(self, data, namespace):
        deployment_list = []
        for key, deployment in data.items():
            deployment_list.append(
                [deployment.order_seq,
                 deployment.name,
                 deployment.service_name,
                 deployment.pod,
                 '✓' if deployment.stateful_set else '▢',
                 '✓' if deployment.selected else '▢',
                 ])
        print(f"Deployments for namespace: {color_text(BGREEN_TEXT, namespace)}")
        headers = ["Order", "Deployment Name", "Service Name", "Pod Name", "StatefulSet", "Selected"]
        print(tabulate(deployment_list, headers=headers, stralign="left"))

    """
    #################### Watcher Service ##################################################################
    """

    def list_resources(self, namespace: str, resources):
        if namespace is None:
            raise MissingNamespaceConfigurationException()

        try:
            statefulset_list = self.client.api.list_namespaced_stateful_set(namespace, pretty="true")
            deployment_list = self.client.api.list_namespaced_deployment(namespace, pretty="true")

            for statefulset in statefulset_list.items:
                if statefulset.metadata.name not in resources:
                    resources[statefulset.metadata.name] = self.add_resources(statefulset, statefulset=True)
                resources[statefulset.metadata.name].metadata = statefulset.metadata
                resources[statefulset.metadata.name].status = statefulset.status

            for deployment in deployment_list.items:
                if deployment.metadata.name not in resources:
                    resources[deployment.metadata.name] = self.add_resources(deployment)
                resources[deployment.metadata.name].metadata = deployment.metadata
                resources[deployment.metadata.name].status = deployment.status

            return resources
        except Exception as e:
            print(f"Error fetching resources in namespace {namespace}: {e}")
            return None

    def list_namespaces_with_current(self):
        return self.client.get_namespaces(), self.config_service.get_config().namespace
