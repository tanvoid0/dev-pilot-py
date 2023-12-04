from py_helper.processor.commander import Commander
from py_helper.utility.regex_util import RegexUtil


class KubernetesCommandStringGenerator:
    @staticmethod
    def scale(namespace, deployment_name, stateful_set, down=False) -> str:
        return f"kubectl scale -n {namespace} {'statefulset' if stateful_set else 'deployment'} {deployment_name} --replicas={'0' if down else '1'};"

    """
    Response:
    Kubernetes control plane is running at https://xx.xxx.xxx.xxx
    GLBCDefaultBackend is running at https://xx.xxx.xxx.xxx/api/v1/namespaces/kube-system/services/default-http-backend:http/proxy
    KubeDNS is running at https://xx.xxx.xxx.xxx/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
    Metrics-server is running at https://xx.xxx.xxx.xxx/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy

    """

    @staticmethod
    def get_ip():
        ip_string = Commander.execute("kubectl cluster-info")
        return RegexUtil.find_first_in_string(ip_string, r'(?:https?:\/\/)(?:\d{1,3}\.){3}\d{1,3}')

    """
    Returns Token.
    Beware of the \\n.
    Check before usage
    """

    @staticmethod
    def get_token():
        return "kubectl -n kube-system describe secret default | awk '$1==\"token:\"{print $2}'"

    @staticmethod
    def get_pods(namespace):
        return f"kubectl get pods -n {namespace}"

    @staticmethod
    def get_jobs(namespace):
        return f"kubectl get jobs -n {namespace}"

    # Delete jobs
    # Success: job.batch "job_name" deleted
    # failure: Error from server (NotFound): jobs.batch "job_name" not found
    @staticmethod
    def delete_job(job_name, namespace):
        return f"kubectl delete -n {namespace} job {job_name}"
