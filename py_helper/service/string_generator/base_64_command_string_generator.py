class Base64CommandStringGenerator:
    @staticmethod
    def encode(data) -> str:
        return f"echo '{data}' | base64"

    @staticmethod
    def decode(data) -> str:
        return f"echo '{data}' | base64 --decode"
