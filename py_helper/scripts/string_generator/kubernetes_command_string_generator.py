class KubernetesCommandStringGenerator:
    @staticmethod
    def scale(namespace, deployment_name, stateful_set, down=False) -> str:
        return f"kubectl scale -n {namespace} {'statefulset' if stateful_set else 'deployment'} {deployment_name} --replicas={'0' if down else '1'};"
