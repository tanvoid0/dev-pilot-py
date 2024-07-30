class DockerCommandStringGenerator:
    @staticmethod
    def build(path, image) -> str:
        return f"cd {path} && docker build --network=host --tag {image} ."

    @staticmethod
    def push(path, image) -> str:
        return f"cd {path} && docker push {image}"

    def build_and_push(path, image) -> str:
        return f"cd {path} && docker build --network=host --tag {image} . && cd {path} && docker push {image}"
