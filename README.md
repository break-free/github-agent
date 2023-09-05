# `github-agent` Demonstration

This github agent is intended to create pull requests and/or manage github
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
> installed on this GitHub repository. The following assumes that this
> app is in use.

1. Create a private key for the GitHub app from the [app's settings](https://github.com/organizations/break-free/settings/apps/breakfree-github-agent-app)
then scroll down to *Private Keys* and hit *Generate a private key*. This will
download a new `*.pem` key file for use. Save this local to this code base
(i.e., in the `github-agent` folder).

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
> If you wish to set up your own GitHub app, then you can either write your own
> (see [here](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps))
> or you can follow a [quickstart tutorial](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/quickstart). Then you must
> [register the application](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app) and then
> [install the application for your repository that you want the agent to manage](https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app).


# Demonstration

Executing the following command runs the demonstration:

```bash
python3 main.py
```

This will:

- Create a new branch.
- Load the `README.md` of the `github-agent-demo` repository.
- Re-write the `README.md`.
- Commit to the `bot-branch` and create a pull request to `main`.


## Cleaning up between demonstrations


### Option 1

To clean up between demonstrations:

- From GitHub, delete the new branch; it will have a randomized five-letter
name. Also, close the created pull request from `bot-branch` to `main` and do
not delete the branch.
- From the console/command line, reset the head of the `bot-branch`:

```bash
git fetch
git checkout -b <GITHUB_BRANCH>
git pull
git log  # Optional
git reset --hard HEAD~1
git push --force --set-upstream origin <GITHUB_BRANCH>
```

Note that for successive resets only the last three commands are required and
change to:

```bash
git pull
git log  # Optional
git reset --hard HEAD~1
git push --force
```

> [!WARNING]
> Using git reset is a dangerous maneuver and should never be attempted on
> `main`, hence the use of `bot-branch`. If it gets out of control, then you
> can delete and re-create the `bot-branch` (and any other branches). This
> resets the branch and the demonstration.


### Option 2

- If you request the agent to create a pull request on your behalf, you'll very
likely need to manually merge and/or close the pull request before proceeding to
any future changes. [See Current Known Limitations](#current-known-limitations)


The `main.py` script installs any custom tools configured in the
`custom_tools.py`.

Within the `main.py` you can adjust the request(s) for the agent to complete.
For example, to make 3 individual requests to the LLM to:

1. Add a new movie quote and separate any existing movie quotes with a newline
1. Create a randomly named 5-letter feature branch
1. Grab the latest commit hash from the 'main' branch

You could use the below:

```python
requests = [
    f"Add a single movie quote to the 'Movie Quotes' section in the README.md. Place a new line between any existing movie quotes and your new one. Then create a pull request to {gh_base_branch} with any changes. Do not create a new branch if the pull request fails."
    ,f"Make a new feature branch called '{''.join(random.choices(string.ascii_letters, k=5))}'" # Make a random 5-letter feature branch
    f"Give me the latest commit from  the 'main' branch"
    ]

for request in requests:
    print(f"Running against the request:\n\n{request}\n")
    agent.run(request)
```

Then run `main.py` and watch the sparks fly


# Tips & Tricks

- When requesting edits be made to a file, be sure to include "once" in the
prompt, else it may make several duplicate edits. Sometimes thousands. Yes you
read that correctly -- **thousands**.

- If, for whatever reason, there is a change in a pull request you DON'T want to
be included from `GITHUB_BRANCH` to the `GITHUB_BASE_BRANCH`, you will likely
need to manually intervene & revert the change on `GITHUB_BRANCH` before
continuing. Occasionally deleting a pull request is enough, but usually not
because each subsequent edit starts from `GITHUB_BASE_BRANCH`. For example to
reset `GITHUB_BRANCH` that has only **one** change:


# Current Known Limitations

- The general workflow for any changes the agent attempts seems to be

    1. Read a file's contents based on the current state of the
    `GITHUB_BASE_BRANCH`, which ultimately serves as the merge destination. THIS
    DOES NOT USE COMMIT HASHES, TRULY JUST A READ FROM THE BASE FILE (a la
    `curl` or `wget`)

    1. Commit any changes to the `GITHUB_BRANCH` based on its original findings
    of the value of the file(s) from `GITHUB_BASE_BRANCH`
  
        - This can setup some odd problems, especially if a change is made in
        the `GITHUB_BRANCH` that doesn't get accepted into the
        `GITHUB_BASE_BRANCH` because the agent doesn't REALLY have any knowledge
        of the commit history within its `GITHUB_BRANCH` and will get version
        conflict errors

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
