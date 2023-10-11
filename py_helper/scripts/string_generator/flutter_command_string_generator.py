class FlutterCommandStringGenerator:
    @staticmethod
    def doctor():
        return "flutter doctor"

    @staticmethod
    def pub_get_packages(path):
        return f"cd {path} && flutter pub get"

    @staticmethod
    def clean_build_models(path):
        return f"cd {path} && flutter packages pub run build_runner build --delete-conflicting-outputs"
