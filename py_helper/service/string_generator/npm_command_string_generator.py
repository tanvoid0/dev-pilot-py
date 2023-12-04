class NpmCommandStringGenerator:
    @staticmethod
    def install(path) -> str:
        return f"cd {path} && npm install"

    @staticmethod
    def clean_install(path) -> str:
        return f"cd {path} && npm ci"

    @staticmethod
    def start(path) -> str:
        return f"cd {path} && npm run start"

    @staticmethod
    def test(path) -> str:
        return f"cd {path} && npm run test"

    @staticmethod
    def lint(path) -> str:
        return f"cd {path} && npm run lint"

    @staticmethod
    def build(path) -> str:
        return f"cd {path} && npm run build"
