from py_helper.models.option_model import OptionGroupModel, OptionModel
from py_helper.service.git_service import GitService
from py_helper.service.project_service import ProjectService


class GitScript(OptionGroupModel):
    project_service = ProjectService()
    git_service = GitService()

    def __init__(self):
        super().__init__(
            "Git Commands",
            [
                OptionModel("gr", "Git remote", "shows remote urls linked to git repository",
                            self.git_service.remote_link_generate),
                OptionModel("gs", "Git Status", "", self.git_service.status),
                OptionModel("gc", "Git Checkout Branch", "", self.git_service.checkout_branch),
            ]
        )
