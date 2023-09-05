import os
from langchain.agents import tool
from github import Github
from github import Auth

@tool
def create_branch(new_branch:str):
    """
    Create a new git branch from the provided repository
    """

    auth = Auth.Token(os.environ["GH_AUTH_TOKEN"])
    
    g = Github(auth=auth)

    repo = os.environ["GITHUB_REPOSITORY"]
    current_branch = os.environ["GITHUB_BRANCH"] # Make sure we're always pulling from the bot's branch
    
    repository = g.get_repo(full_name_or_id=repo)
    branch = repository.get_branch(current_branch)
    head = branch.commit

    # print(f"Repo:{repository.name}\n\nBranch:{branch.name}\n\nHead Commit sha:{head.sha}")

    repository.create_git_ref(ref=f"refs/heads/{new_branch}", sha=head.sha)

    return f"New branch: {new_branch}"

@tool
def get_latest_commit(branch:str):
    """
    Get the latest commit sha
    """

    auth = Auth.Token(os.environ["GH_AUTH_TOKEN"])
    
    g = Github(auth=auth)

    repo = os.environ["GITHUB_REPOSITORY"]
    current_branch = os.environ["GITHUB_BRANCH"]
    
    repository = g.get_repo(full_name_or_id=repo)
    branch = repository.get_branch(current_branch)
    head = branch.commit

    return head
    
# # List of required environment variables:
# env_vars = [
#     "GITHUB_APP_ID",
#     "GITHUB_APP_PRIVATE_KEY",
#     "GITHUB_REPOSITORY",
#     "GITHUB_BRANCH",
#     "GITHUB_BASE_BRANCH",
#     "OPENAI_API_KEY",
#     "GH_AUTH_TOKEN"
# ]

# # Check your json file for key values
# with open("envvars.json", "r") as f:
#     env_var_values = json.load(f)

# for var in env_vars:
#     # Check that each key exists. If it doesn't, set it to be "" and then complain later
#     if env_var_values.get(var, "") != "": 
#         os.environ[var] = env_var_values[var]
#     else: # Complaint line
#         raise Exception(f"The environment variable {var} was not set. You must set this value to continue.")


# create_branch(new_branch="hello")
