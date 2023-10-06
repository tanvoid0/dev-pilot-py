class MavenCommandStringGenerator:
    @staticmethod
    def clean_install(path, without_tests=False):
        return f"cd {path} && mvn clean install {'-DskipTests=True' if without_tests else ''}"

    @staticmethod
    def test(path):
        return f"cd {path} && mvn run test"
