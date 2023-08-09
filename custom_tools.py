import os
from langchain.agents import tool
from googlesearch import search
from github import Github
from github import Auth
import json

# @tool
# def search_online(input:str):
#     """
#     Search online for and return the very first link found from an input term or phrase.
#     """
    
#     # Just a limitation of the package used; if you don't use a list it'll provide a generator class instead of a string:
#     result = list(search(term=input, num_results=1))
        
#     return result[0]

@tool
def create_branch(new_branch:str):
    """
    Create a new git branch from the provided repository
    """

    auth = Auth.Token(os.environ["GH_AUTH_TOKEN"])
    
    g = Github(auth=auth)

    repo = os.environ["GITHUB_REPOSITORY"]
    current_branch = os.environ["GITHUB_BRANCH"]
    
    repository = g.get_repo(full_name_or_id=repo)
    branch = repository.get_branch(current_branch)
    head = branch.commit

    # print(f"Repo:{repository.name}\n\nBranch:{branch.name}\n\nHead Commit sha:{head.sha}")

    # repository.create_git_ref(ref=f"refs/head/{new_branch}", sha=head.sha)
    repository.create_git_ref(ref=f"refs/heads/{new_branch}", sha=head.sha)
    # repository.merge(base=)
    
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