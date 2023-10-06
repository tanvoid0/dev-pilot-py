import os

from py_helper.processor.os_commander import OSCommander


class CommandStringGenerator:
    @staticmethod
    def launch_notepad(file_path):
        return OSCommander.run(
            linux=lambda: f"xdg-open {file_path}"
        )

    @staticmethod
    def ping(domain):
        return OSCommander.run(
            linux=lambda: f"ping -c 5 {domain}",
            windows=lambda: f"ping -n 5 {domain}"
        )

    @staticmethod
    def remove_subdirectories(path):
        return OSCommander.run(
            linux=lambda: f"rm -rf {os.path.join(path, '*')}"
        )

    @staticmethod
    def kubernetes_scale(namespace, deployment_name, down=False, stateful_set=False):
        return OSCommander.run(
            common=lambda: f"kubectl scale -n {namespace} {'statefulset' if stateful_set else 'deployment'} {deployment_name} --replicas={'0' if down else '1'};"
        )

    @staticmethod
    def kubernetes_apply_deployment_config(file_path, namespace):
        return OSCommander.run(
            common=lambda: f"kubectl apply deployment -f {file_path} -n {namespace}"
        )
