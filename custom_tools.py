import os
from langchain.tools import BaseTool
from github import Github
from github import Auth


class CreateBranch(BaseTool):

    name = "Create GitHub Branch Tool"
    description = (
        "use this tool to create a new branch"
    )

    def _run(self, new_branch: str):

        auth = Auth.Token(os.environ["GH_AUTH_TOKEN"])
        repo_url = os.environ["GITHUB_REPOSITORY"]
        repository = Github(auth=auth).get_repo(full_name_or_id=repo_url)
        branch = repository.get_branch(os.environ["GITHUB_BASE_BRANCH"])
        head = branch.commit

        repository.create_git_ref(ref=f"refs/heads/{new_branch}", sha=head.sha)

        return f"New branch: {new_branch}"

    def _arun(self, new_branch: str):
        raise NotImplementedError("This tool does not support async")
