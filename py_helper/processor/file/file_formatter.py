# import ruamel.yaml
#
# yaml = ruamel.yaml.YAML()
# yaml.preserve_quotes = True
import yaml


class FileFormatter:
    @staticmethod
    def format_yaml(file):
        return yaml.safe_load(file)
