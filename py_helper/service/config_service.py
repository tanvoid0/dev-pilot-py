from sqlalchemy.orm import joinedload

from py_helper.models.config_file_model import ConfigFileModel
from py_helper.models.config_model import ConfigModel
from py_helper.models.exception.config_not_initialized_exception import ConfigNotInitializedException
from py_helper.processor.commander import Commander
from py_helper.processor.db_processor import DBProcessor
from py_helper.processor.print_processor import color_text, GREEN_TEXT
from py_helper.service.config_file_service import ConfigFileService
from py_helper.service.string_generator.kubernetes_command_string_generator import KubernetesCommandStringGenerator


class ConfigService:
    db = DBProcessor()
    config_file_service = ConfigFileService()

    def first_time_setup(self):
        try:
            config_data = self.config_file_service.create_config_file_from_example_file()
            db_file_does_not_exist = self.config_file_service.create_db_file_if_doesnt_exist(config_data['db_reset']) # TODO: update when create_config_file_from_example_file is fixed
            if not db_file_does_not_exist:
                return True
            self.db.initiate_data()
            self.create_first_config()
            return False
        except Exception as ex:
            print(ex)
            raise ex

    def create_first_config(self):
        config_data = self.config_file_service.get_config_file()
        session = self.db.get_session()
        config = self.get_config(safe_load=True)
        if config is not None:
            return
        # namespace = self.kubernetes_service.select_namespace()
        # namespace = config_data.kubernetes.namespace
        docker_pre_tag = config_data.kubernetes.docker_pre_tag
        docker_post_tag = "latest"
        kubernetes_ip = KubernetesCommandStringGenerator.get_ip()
        kubernetes_token = Commander.execute(KubernetesCommandStringGenerator.get_token())
        kubernetes_token = kubernetes_token.replace('\n', '')
        runtime_var = ConfigModel(
            # namespace=namespace,
            docker_pre_tag=docker_pre_tag,
            docker_post_tag=docker_post_tag,
            kubernetes_ip=kubernetes_ip,
            kubernetes_token=kubernetes_token,
            scale_up_timeout=config_data.kubernetes.scale.up,
            scale_down_timeout=config_data.kubernetes.scale.down,

            vpn_username=config_data.vpn.username,
            vpn_password=config_data.vpn.password,
            vpn_config=config_data.vpn.config_file
        )
        session.add(runtime_var)
        session.commit()
        print("Runtime vars " + color_text(GREEN_TEXT, "configured..."))

    def get_config(self, safe_load=False) -> ConfigModel:
        session = self.db.get_session()
        config = (session.query(ConfigModel).filter_by(id=1)
                  .options(joinedload(ConfigModel.project))
                  .first())
        if config is None and not safe_load:
            raise ConfigNotInitializedException()
        return config

    def get_config_file(self) -> ConfigFileModel:
        return self.config_file_service.get_config_file()

    def update_project(self, project_id):
        session = self.db.get_session()
        model = session.query(ConfigModel).get(1)
        model.project_id = project_id
        session.commit()
        return model

    def update_namespace(self, namespace):
        session = self.db.get_session()
        model = session.query(ConfigModel).get(1)
        model.namespace = namespace
        if model.docker_post_tag != "latest":
            model.docker_post_tag = namespace
        session.commit()
        return model

    def toggle_docker_tag(self, docker_pre_tag, docker_post_tag):
        session = self.db.get_session()
        model = session.query(ConfigModel).get(1)
        model.docker_pre_tag = docker_pre_tag
        model.docker_post_tag = docker_post_tag
        session.commit()
        return model

    def get_current_docker_image(self) -> str | None:
        session = self.db.get_session()
        model = session.query(ConfigModel).get(1)
        if model.project is None:
            return None
        return f"{model.docker_pre_tag}/{model.project.name}:{model.docker_post_tag}"
