import os
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.utilities.github import GitHubAPIWrapper
import json
import custom_tools

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
    
bot_branch = os.environ["GITHUB_BRANCH"]
gh_base_branch = os.environ["GITHUB_BASE_BRANCH"]
    
llm = ChatOpenAI(model="gpt-4")
github = GitHubAPIWrapper()
toolkit = GitHubToolkit.from_github_api_wrapper(github)

tools = []

# unwanted_tools = ['Get Issue','Delete File']
unwanted_tools = []
for tool in toolkit.get_tools():
    if tool.name not in unwanted_tools:
        tools.append(tool)

# tools.append(custom_tools.search_online)

agent = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# request = f"Search online for documentation about Github Applications and place their links in the 'References' section of the root README.md file. Open a pull request into {gh_base_branch} for any changes."
request = f"Search online for documentation about Artificial Intelligence and place their links in the 'References' section of the root README.md file. Open a pull request into {gh_base_branch} for any changes."
# request = f"Start a new git branch from {bot_branch}. Then, search online for documentation about macaroni & cheese and place their links in the 'Culinary' section of the root README.md file. Open a pull request from your new feature branch into {gh_base_branch} for any changes."

agent.run(request)