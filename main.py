import os
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.llms import OpenAI
from langchain.utilities.github import GitHubAPIWrapper
import json

# List of required environment variables:
env_vars = [
    "GITHUB_APP_ID",
    "GITHUB_APP_PRIVATE_KEY",
    "GITHUB_REPOSITORY",
    "GITHUB_BRANCH",
    "GITHUB_BASE_BRANCH",
    "OPENAI_API_KEY"
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
    
llm = OpenAI(temperature=0)
github = GitHubAPIWrapper()
toolkit = GitHubToolkit.from_github_api_wrapper(github)

tools = []
unwanted_tools = ['Get Issue','Delete File', 'Create File']

for tool in toolkit.get_tools():
    if tool.name not in unwanted_tools:
        tools.append(tool)

agent = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# request = "You have the software engineering capabilities of a Google Principle engineer. You are tasked with completing issues on a github repository. Please look at the existing issues and complete them."
request = "Find relevant Github Application Documentation and place their documentation in the 'References' section of the root README.md file. Open a pull request into main for any changes."

agent.run(request)