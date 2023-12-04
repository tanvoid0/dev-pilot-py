class GitCommandStringGenerator:
    @staticmethod
    def get_remote(path):
        return f"cd {path} && git remote -v"

    @staticmethod
    def status(path):
        return f"cd {path} && git status"

    @staticmethod
    def switch_branch(path: str, branch_name: str):
        return f"cd {path} && git switch -c {branch_name}"
