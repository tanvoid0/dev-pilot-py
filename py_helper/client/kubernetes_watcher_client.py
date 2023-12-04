import threading

from kubernetes import watch, client, config


class KubernetesWatcherClient:
    config.load_kube_config()
    api_instance = client.AppsV1Api()

    # Function to watch for changes in deployments
    def watch_deployments(self, namespace, resources, watching):
        print(f"Watch Deployment value: {watching}")
        w = watch.Watch()
        api_instance = client.AppsV1Api()
        resource_version = ""

        while watching:
            try:
                stream = w.stream(api_instance.list_namespaced_deployment, namespace, resource_version=resource_version)
                print(f"Inside stream")
                for event in stream:
                    if event['type'] == 'ADDED' or event['type'] == 'MODIFIED':
                        print(f"Inside event")
                        resource = event['object']
                        resource_name = resource.metadata.name
                        resources[resource_name] = resource
                        resource_version = resource.metadata.resource_version
                        print(f"Deployment {resource_name} has been {event['type']}.")
            except Exception as e:
                print(f"Error watching deployments in namespace {namespace}: {e}")

    # Function to watch for changes in stateful sets
    def watch_statefulsets(self, namespace, resources, watching):
        w = watch.Watch()
        api_instance = client.AppsV1Api()
        resource_version = ""

        while watching:
            try:
                stream = w.stream(api_instance.list_namespaced_stateful_set, namespace,
                                  resource_version=resource_version)
                for event in stream:
                    if event['type'] == 'ADDED' or event['type'] == 'MODIFIED':
                        resource = event['object']
                        resource_name = resource.metadata.name
                        resources[resource_name] = resource
                        resource_version = resource.metadata.resource_version
                        print(f"StatefulSet {resource_name} updated.")
            except Exception as e:
                print(f"Error watching stateful sets in namespace {namespace}: {e}")

    def reset_watcher(self, resources, list_fetcher):
        resources.clear()
        resources.update(list_fetcher)
        return resources

    def run(self, initial_namespace="jay"):
        config.load_kube_config()

        resources = {}
        print(f"Watching resources in namespace {initial_namespace}")
        resources.update(self.list_resources(initial_namespace))

        deployment_thread = threading.Thread(target=self.watch_deployments, args=(initial_namespace, resources))
        statefulset_thread = threading.Thread(target=self.watch_statefulsets, args=(initial_namespace, resources))

        deployment_thread.start()
        statefulset_thread.start()

        while True:
            user_namespace = input("Enter a new namespace to watch (or press Enter to exit): ")
            if user_namespace == "":
                break
            resources = self.reset_watcher(user_namespace, resources)
