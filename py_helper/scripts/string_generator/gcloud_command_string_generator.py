class GCloudCommandStringGenerator:
    @staticmethod
    def login() -> str:
        return "gcloud auth login"

    @staticmethod
    def init_gcloud() -> str:
        return "gcloud init"
