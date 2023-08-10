# github-tool
Start on Github AI Tool

## Overview

### Setup
Start with a ./envvars.json like this (fill out actual values):
```
{
    "GITHUB_APP_ID": "A six digit number found in your app's general settings",
    "GITHUB_APP_PRIVATE_KEY": "The location of your app's private key .pem file",
    "GITHUB_REPOSITORY": "The name of the Github repository you want your bot to act upon. Must follow the format {username}/{repo-name}. Make sure the app has been added to this repository first!",
    "GITHUB_BRANCH": "The branch where the bot will make its commits. Defaults to 'master.'",
    "GITHUB_BASE_BRANCH": "The base branch of your repo, usually either 'main' or 'master.' This is where pull requests will base from. Defaults to 'master.'"
    "GH_AUTH_TOKEN": "User Credentials to allow more nuanced GH commands. Unsure if it's really necessary yet."
    "OPENAI_API_KEY": "The API Key used for communicating with OpenAI."
}
```