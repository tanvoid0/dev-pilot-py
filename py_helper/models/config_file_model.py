class _VPNConfigFileModel:
    username: str
    password: str
    config_file: str

    def __init__(self, username=None, password=None, config_file=None):
        self.username = username
        self.password = password
        self.config_file = config_file


class KubernetesScaleConfigFileModel:
    up: int
    down: int

    def __init__(self, up=30, down=5):
        self.up = up
        self.down = down


class _KubernetesConfigFileModel:
    docker_pre_tag: str
    docker_pre_tag_latest: str
    scale: KubernetesScaleConfigFileModel

    def __init__(self, docker_pre_tag=None, docker_pre_tag_latest=None, scale=KubernetesScaleConfigFileModel()):
        self.docker_pre_tag = docker_pre_tag
        self.docker_pre_tag_latest = docker_pre_tag_latest
        self.scale = scale


class ConfigFileModel:
    db_reset: bool
    startup_time: int
    vpn: _VPNConfigFileModel
    kubernetes: _KubernetesConfigFileModel

    def __init__(self, db_reset=False, startup_time=0, vpn=_VPNConfigFileModel(),
                 kubernetes=_KubernetesConfigFileModel()):
        self.db_reset = db_reset
        self.startup_time = startup_time
        self.vpn = vpn
        self.kubernetes = kubernetes

    def to_json(self):
        return {
            'db_reset': self.db_reset,
            'startup_time': self.startup_time,
            'vpn': {
                'username': self.vpn.username,
                'password': self.vpn.password,
                'config_file': self.vpn.config_file,
            },
            'kubernetes': {
                'docker_pre_tag': self.kubernetes.docker_pre_tag,
                'docker_pre_tag_latest': self.kubernetes.docker_pre_tag_latest,
                'scale': {
                    'up': self.kubernetes.scale.up,
                    'down': self.kubernetes.scale.down,
                }
            }
        }

    @staticmethod
    def from_json(json):
        return ConfigFileModel(
            db_reset=json['db_reset'],
            startup_time=json['startup_time'],
            vpn=_VPNConfigFileModel(
                username=json['vpn']['username'],
                password=json['vpn']['password'],
                config_file=json['vpn']['config_file']
            ),
            kubernetes=_KubernetesConfigFileModel(
                docker_pre_tag=json['kubernetes']['docker_pre_tag'],
                docker_pre_tag_latest=json['kubernetes']['docker_pre_tag_latest'],
                scale=KubernetesScaleConfigFileModel(
                    up=json['kubernetes']['scale']['up'],
                    down=json['kubernetes']['scale']['down'],
                )
            )
        )
