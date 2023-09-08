import custom_tools
import json
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.utilities.github import GitHubAPIWrapper
import os
import random
import string

# Check your json file for key values
with open("envvars.json", "r") as f:
    env_vars = json.load(f)

for key, value in env_vars.items():
    if value != "":
        os.environ[key] = value
    else:
        raise Exception(
            f"""The environment variable '{key}' was not set. You must """
            f"""set this value to continue."""
        )

main_branch = os.environ["GITHUB_BASE_BRANCH"]
new_branch = 'fix_' + ''.join(random.choices(string.ascii_letters, k=5))
os.environ["GITHUB_BRANCH"] = new_branch

github = GitHubAPIWrapper()
toolkit = GitHubToolkit.from_github_api_wrapper(github)
tools = [] + toolkit.get_tools()
tools.append(custom_tools.CreateBranch())

agent = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=ChatOpenAI(model="gpt-4", temperature=0),
    memory=ConversationBufferWindowMemory(k=5),
    tools=tools,
    verbose=True,
)

agent.run(
    f"""In a new branch '{new_branch}' from '{main_branch}', edit the 'README.md' to add a new 'Movie Quote' section with one movie quote at the end of the file, then create a pull request to merge."""
)
