class DockerCommandStringGenerator:
    @staticmethod
    def build(path, image) -> str:
        return f"cd {path} && docker build --network=host --tag {image} ."

    @staticmethod
    def push(path, image) -> str:
        return f"cd {path} && docker push {image}"
