# `github-agent` Demonstration

This GitHub agent is intended to create pull requests and/or manage github
repositories as part of chains.

# Setup

## Environment

## Application

The agent is configured against two branches, the `GITHUB_BASE_BRANCH` (default
branch) and a separate `GITHUB_BRANCH` that should be considered "dedicated" for
the agent to make commits.

> [!WARNING]
> Be sure to use a `*.json` file as your environment file to avoid publishing
> API keys and other sensitive secrets to GitHub. The `.gitignore` in this repo
> ignores `*.json` from being accidentally committed.

> [!NOTE]
> BreakFree already has an GitHub app called `breakfree-github-agent-app`
> installed on a `github-agent-demo`  repository. The following assumes that
> this repository and app is in use.

1. Create a private key for the GitHub app from the [app's settings](https://github.com/organizations/break-free/settings/apps/breakfree-github-agent-app)
then scroll down to *Private Keys* and hit *Generate a private key*. This will
download a new `*.pem` key file for use. Save this local to this code base,
i.e., in the `github-agent` folder.

1. Create a personal access token. To do so:

    - Select your user profile (top-right) then select *Settings*.
    - Select *Developer settings*.
    - Expand *Personal access tokens* and then select *Tokens (classic)*.
    - From the *Generate new token* menu, select *... (classic)*.
    - Add "breakfree-github-agent" (or similar) to *Note*
    - Set *Expiration* (default is 30 days) as needed.
    - Select the following scopes (and all associated child scopes): *repo*,
    *workflow*, *gist*, *notifications*, *user*, *write:discussion*,
    *audit_log*, *codespace*, and *project*.
    - Finally select *Generate token* at the bottom of the page.

1. Create a new or use an existing OpenAI key using [this guide](https://breakfree.atlassian.net/wiki/spaces/BFAIML/pages/2289369089/Using+the+BreakFree+OpenAI+Account).

1. Create a `envvars.json` like the below. Values for `GITHUB_APP_PRIVATE_KEY`,
`GH_AUTH_TOKEN`, and `OPENAI_API_KEY` (as created/used above) are required. All
other values are provided when using the default BreakFree GitHub app.

```json
{
    "GITHUB_APP_ID": "383948",
    "GITHUB_APP_PRIVATE_KEY": "Your app's private key .pem file location; if the location is the local directory just add `<filename>.pem`",
    "GITHUB_REPOSITORY": "break-free/github-agent-demo",
    "GITHUB_BRANCH": "bot-branch",
    "GITHUB_BASE_BRANCH": "main",
    "GH_AUTH_TOKEN": "User Credentials to allow more nuanced GH commands. Unsure if it's really necessary yet, but is currently being used for actions not available out-of-box like creating a new git branch.",
    "OPENAI_API_KEY": "The API Key used for communicating with OpenAI."
}
```

> [!NOTE]
> To review how the GitHub app was setup, see [creating GitHub apps](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps))
> and the [quickstart tutorial](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/quickstart). Then review [register the application](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app)
> and [install the application for your repository that you want the agent to manage](https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app).


# Demonstration

Executing the following command runs the demonstration:

```bash
python3 main.py
```

This will:

- Create a new branch at `github-agent-demo`
- Edit the `README.md` to include a movie quote.
- Commit to a `fix_XXXXX` branch (where XXXXX is randomized)
- Create a pull request to `main`.

Note that the `main` branch is read-only, and pull requests will not succeed.
`main` branch was protected on purpose to keep the repository pristine.

## Cleaning up between demonstrations

To clean up between demonstrations, [from GitHub delete the new branch](https://github.com/break-free/github-agent-demo/branches);
it will have a randomized five-letter name. You will need to confirm the
deletion.

# Tips & Tricks

- When requesting edits be made to a file, be sure to include "once" in the
prompt, else it may make several duplicate edits. Sometimes thousands. Yes you
read that correctly -- **thousands**.

# Current Known Limitations

- The general workflow for any changes the agent attempts seems to be

    1. Read a file's contents based on the current state of the
    `GITHUB_BASE_BRANCH`, which ultimately serves as the merge destination. THIS
    DOES NOT USE COMMIT HASHES, TRULY JUST A READ FROM THE BASE FILE (a la
    `curl` or `wget`)

- The Langchain Github agent is really only configured to communicate over two
branches out-of-box and requires additional configuration/tooling to be able to
communicate with different branches

# TODO as part of BAM-594

These are simply the tasks / direction Zak was headed when he last worked on
this project. Feel free to adjust direction, steps, methods, or any other
decisions as you see fit. It doesn't even need to be in this project if it feels
like an easier approach could be taken.

- [ ] Create a for loop in `main.py` that detects all tools within the
`custom_tools.py` so that we can append them to being available to the agent
- [ ] Have a `new_tool.py` 'module' available to the agent that writes a new
function back to the `custom_tools.py`

# Future Work

- Allow multiple commits before requiring a pull request from `GITHUB_BRANCH` to
`GITHUB_BASE_BRANCH`
- Experiment with different types of agents to allow multi-parameter custom
tools
