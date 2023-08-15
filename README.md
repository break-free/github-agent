# Overview
This github agent is intended to create pull requests and/or manage github repositories as part of chains.

The agent is configured against two branches, the `GITHUB_BASE_BRANCH` (default branch) and a separate `GITHUB_BRANCH` that should be considered "dedicated" for the agent to make commits.

# Setup
> [!WARNING]  
> Be sure to use a json file as your environment file to avoid publishing API keys and other sensitive secrets to github. The `.gitignore` in this repo ignores `*.json` from being accidentally committed.

First, you will need to setup a Github Application. At a high level:
* [Register the application](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app)

* Create an application. You can either write your own (see [here](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps)) or you can follow a [quickstart tutorial](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/quickstart). 
> [!NOTE]  
> The functionality/code of the application likely will not actually be consumed by the agent, but you need to create an application for the agent to consume

* [Install the application for your repository that you want the agent to manage](https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app)

* Create a `envvars.json` like this (fill out actual values):
```
{
    "GITHUB_APP_ID": "A six digit number found in your app's general settings",
    "GITHUB_APP_PRIVATE_KEY": "The location of your app's private key .pem file",
    "GITHUB_REPOSITORY": "The name of the Github repository you want your bot to act upon. Must follow the format {username}/{repo-name}. Make sure the app has been added to this repository first!",
    "GITHUB_BRANCH": "The branch where the bot will make its commits. Defaults to 'master.'",
    "GITHUB_BASE_BRANCH": "The base branch of your repo, usually either 'main' or 'master.' This is where pull requests will base from. Must match the repository's Default Branch. This value defaults to 'master.'"
    "GH_AUTH_TOKEN": "User Credentials to allow more nuanced GH commands. Unsure if it's really necessary yet."
    "OPENAI_API_KEY": "The API Key used for communicating with OpenAI."
}
```

# Simple Usage
The `main.py` script installs any custom tools configured in the `custom_tools.py`. 

Within the `main.py` you can adjust the request(s) for the agent to complete. For example, to make 3 individual requests to the LLM to 
1. Add a new movie quote and separate any existing movie quotes with a newline
2. Create a randomly named 5-letter feature branch
3. Grab the latest commit hash from the 'main' branch

You could use the below:

```
requests = [
    f"Add a single movie quote to the 'Movie Quotes' section in the README.md. Place a new line between any existing movie quotes and your new one. Then create a pull request to {gh_base_branch} with any changes. Do not create a new branch if the pull request fails."
    ,f"Make a new feature branch called '{''.join(random.choices(string.ascii_letters, k=5))}'" # Make a random 5-letter feature branch
    f"Give me the latest commit from  the 'main' branch"
    ]

for request in requests:
    print(f"Running against the request:\n\n{request}\n")
    agent.run(request)
```

# Tips & Tricks
* When requesting edits be made to a file, be sure to include "once" in the prompt, else it may make several duplicate edits. Sometimes thousands. Yes you read that correctly -- thousands.
* If you request the agent to create a pull request on your behalf, you'll very likely need to manually merge and/or close the pull request before proceeding to any future changes. [See Current Known Limitations](#current-known-limitations)
* If, for whatever reason, there is a change in a pull request you DON'T want to be included from `GITHUB_BRANCH` to the `GITHUB_BASE_BRANCH`, you will likely need to manually intervene & revert the change on `GITHUB_BRANCH` before continuing. Occasionally deleting a pull request is enough, but usually not because each subsequent edit starts from `GITHUB_BASE_BRANCH`.

# Current Known Limitations
* The general workflow for any changes the agent attempts seems to be 
  - Read a file's contents based on the current state of the `GITHUB_BASE_BRANCH`, which ultimately serves as the merge destination. THIS DOES NOT USE COMMIT HASHES, TRULY JUST A READ FROM THE BASE FILE (a la `curl` or `wget`)
  - Commit any changes to the `GITHUB_BRANCH` based on its original findings of the value of the file(s) from `GITHUB_BASE_BRANCH`
  
  This can setup some odd problems, especially if a change is made in the `GITHUB_BRANCH` that doesn't get accepted into the `GITHUB_BASE_BRANCH` because the agent doesn't REALLY have any knowledge of the commit history within its `GITHUB_BRANCH` and will get version conflict errors

* The Langchain Github agent is really only configured to communicate over two branches out-of-box and requires additional configuration/tooling to be able to communicate with different branches

* The Langchain Github agent seems to really only work with a user's repo and not necessarily an organization's. 

# Future Work
* Allow multiple commits before requiring a pull request from `GITHUB_BRANCH` to `GITHUB_BASE_BRANCH`
* Allow work on an organization's repository
* Experiment with different types of agents to allow multi-parameter custom tools
