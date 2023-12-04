from kubernetes import client as kube_client, config as kube_config, watch

from py_helper.models.exception.missing_namespace_configuration_exception import MissingNamespaceConfigurationException


class KubernetesClient:
    kube_config.load_kube_config()
    api = kube_client.AppsV1Api()

    @staticmethod
    def live_deployment_portal():
        pass
        # thread = threading.Thread(target=KubernetesClient.execute_function)
        # thread.daemon = True
        # thread.start()
        #
        # while True:
        #     user_input = sys.stdin.readline()
        #
        #     if user_input == "\n":
        #         break
        #
        #     elif user_input == "\b":
        #         continue
        #
        #     else:
        #         thread.join()
        #
        # sys.exit()

    def get_namespaces(self):
        v1 = kube_client.CoreV1Api()
        namespace_list = v1.list_namespace()
        return [namespace.metadata.name for namespace in namespace_list.items]

    def list_resources(self, namespace):
        resources = {}
        api_instance = kube_client.AppsV1Api()

        try:
            deployment_list = api_instance.list_namespaced_deployment(namespace, pretty="true")
            statefulset_list = api_instance.list_namespaced_stateful_set(namespace, pretty="true")

            for deployment in deployment_list.items:
                resources[deployment.metadata.name].metadata = deployment.metadata
                resources[deployment.metadata.name].status = deployment.status
            for statefulset in statefulset_list.items:
                resources[statefulset.metadata.name] = statefulset

            return resources
        except Exception as e:
            print(f"Error fetching resources in namespace {namespace}: {e}")
            return None

    def get_deployments_and_stateful_sets(self, namespace) -> {str: object}:
        resources = {}
        try:
            deployment_list = self.api.list_namespaced_deployment(namespace, pretty=True)
            stateful_set_list = self.api.list_namespaced_stateful_set(namespace, pretty=True)

            # Add a middle process to organise by database order

            for deployment in deployment_list.items:
                resources[deployment.metadata.name] = deployment
            for statefulset in stateful_set_list.items:
                resources[statefulset.metadata.name] = statefulset.metadata

            return resources
        except Exception as ex:
            return None

    def get_stateful_sets(self, namespace):
        stateful_sets = {}
        try:
            stateful_set_list = self.api.list_namespaced_stateful_set(namespace, pretty=True)
            for item in stateful_set_list.items:
                stateful_sets[item.metadata.name] = item
                stateful_sets[item.metadata.name].stateful_set = True
            return stateful_sets
        except Exception as ex:
            return None

    def get_deployments(self, namespace):
        deployments = {}
        try:
            deployment_list = self.api.list_namespaced_deployment(namespace, pretty=True)
            for deployment in deployment_list.items:
                deployments[deployment.metadata.name] = deployment
            return deployments
        except Exception as e:
            return None

    def watch_resources(self, namespace, resources):
        w = watch.Watch()
        deployment_resource_version = ""
        statefulset_resource_version = ""

        while True:
            try:
                statefulset_stream = w.stream(self.api.list_namespaced_stateful_set, namespace,
                                              resource_version=statefulset_resource_version)

                deployment_stream = w.stream(self.api.list_namespaced_deployment, namespace,
                                             resource_version=deployment_resource_version)

                for event in statefulset_stream:
                    if event['type'] == 'ADDED' or event['type'] == 'MODIFIED':
                        resource_name = event['object'].metadata.name
                        resource_metadata = event['object'].metadata
                        resources[resource_name] = resource_metadata
                        statefulset_resource_version = event['object'].metadata.resource_version
                        print(f"StatefulSet {resource_name} updated.")

                for event in deployment_stream:
                    if event['type'] == 'ADDED' or event['type'] == 'MODIFIED':
                        resource_name = event['object'].metadata.name
                        resource_metadata = event['object'].metadata
                        resources[resource_name] = resource_metadata
                        deployment_resource_version = event['object'].metadata.resource_version
                        print(f"Deployment {resource_name} updated.")



            except Exception as ex:
                print(ex)

    def watch_deployments(self, namespace, deployments):
        w = watch.Watch()
        resource_version = ""

        while True:
            try:
                stream = w.stream(self.api.list_namespaced_deployment, namespace, resource_version=resource_version)
                for event in stream:
                    if event['type'] == 'ADDED' or event['type'] == 'MODIFIED':
                        deployment_name = event['object'].metadata.name
                        deployment = event['object']
                        deployments[deployment_name] = deployment
                        resource_version = event['object'].metadata.resource_version
                        print(f"Deployment {deployment_name} has been {event['type']}.")
                        print(event['type'])
                        print(event['object'].status)
            except Exception as ex:
                print(f"Error watching deployments in namespace {namespace}: {ex}")

    def reset_watcher(self, new_namespace, resources):
        resources.clear()
        self.watch_resources(new_namespace, resources)

    def reset_watch_deployments(self, new_namespace, deployments):
        deployments.clear()
        self.watch_deployments(new_namespace, deployments)

    def fetch_deployments_and_stateful_sets_ordered(self, namespace: str):
        if namespace is None:
            raise MissingNamespaceConfigurationException()
        kube_config.load_kube_config()
        app_api_instance = kube_client.AppsV1Api()
        stateful_sets = app_api_instance.list_namespaced_stateful_set(namespace=namespace)
        deployments = app_api_instance.list_namespaced_deployment(namespace=namespace)

        return stateful_sets, deployments

    def get_pods(self, namespace):
        print(f"Listing all pods for namespace {namespace}")
        kube_config.load_kube_config()
        api_instance = kube_client.CoreV1Api()
        pods = api_instance.list_namespaced_pod(namespace=namespace)
        for pod in pods.items:
            print(f"Pod Name: {pod.metadata.name}")

    def get_deployment(self, deployment_name, namespace):
        deployment = kube_client.AppsV1Api().read_namespaced_deployment(deployment_name, namespace)
        if deployment is None:
            print(f"Deployment {deployment_name} not found")
            raise "Deployment not found"
        return deployment

    def get_spec_for_deployment(self, deployment_name: str, namespace: str):
        deployment = self.get_deployment(deployment_name, namespace)
        return deployment.spec
