import os
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.utilities.github import GitHubAPIWrapper
import json
import custom_tools
import string
import random

# List of required environment variables:
env_vars = [
    "GITHUB_APP_ID",
    "GITHUB_APP_PRIVATE_KEY",
    "GITHUB_REPOSITORY",
    "GITHUB_BRANCH",
    "GITHUB_BASE_BRANCH",
    "OPENAI_API_KEY",
    "GH_AUTH_TOKEN"
]

# Check your json file for key values
with open("envvars.json", "r") as f:
    env_var_values = json.load(f)

for var in env_vars:
    # Check that each key exists. If it doesn't, set it to be "" and then complain later
    if env_var_values.get(var, "") != "": 
        os.environ[var] = env_var_values[var]
    else: # Complaint line
        raise Exception(f"The environment variable {var} was not set. You must set this value to continue.")
    
bot_branch = os.environ["GITHUB_BRANCH"]
gh_base_branch = os.environ["GITHUB_BASE_BRANCH"]
    
llm = ChatOpenAI(model="gpt-4")
github = GitHubAPIWrapper()
toolkit = GitHubToolkit.from_github_api_wrapper(github)

tools = []

unwanted_tools = []
for tool in toolkit.get_tools():
    if tool.name not in unwanted_tools:
        tools.append(tool)

tools.append(custom_tools.create_branch)
tools.append(custom_tools.get_latest_commit)

agent = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

requests = [
    f"Add a single movie quote to the 'Movie Quotes' section in the README.md. Place a new line between any existing movie quotes and your new one. Then create a pull request to {gh_base_branch} with any changes. Do not create a new branch if the pull request fails."
    ,f"Make a new feature branch called '{''.join(random.choices(string.ascii_letters, k=5))}'" # Make a random 5-letter feature branch
    f"Give me the latest commit from  the 'main' branch"
    ]

for request in requests:
    print(f"Running against the request:\n\n{request}\n")
    agent.run(request)