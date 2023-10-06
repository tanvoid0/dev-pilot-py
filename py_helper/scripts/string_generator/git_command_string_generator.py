class GitCommandStringGenerator:
    @staticmethod
    def get_remote(path):
        return f"cd {path} && git remote -v"

    @staticmethod
    def status(path):
        return f"cd {path} && git status"
