# from py_helper.service.kubernetes_service import KubernetesService
#
# kubernetes_service = KubernetesService()
#
# initial_namespace = "jay"
# print(f"Watching deployments in namespace {initial_namespace}")
# resources = kubernetes_service.client.get_deployments_and_stateful_sets(initial_namespace)
#
# if resources is not None:
#     kubernetes_service.client.watch_resources(initial_namespace, resources)
#
# while True:
#     user_namespace = input("Enter a new namespace to watch (or press Enter to exit): ")
#     if user_namespace == "":
#         break
#     kubernetes_service.client.reset_watcher(user_namespace, resources)
from py_helper.gui_app.kubernetes_app import KubernetesApp

# KubernetesWatcherClient().run()
KubernetesApp()
