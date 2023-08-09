# github-tool
Start on Github AI Tool

## Overview

### Setup
Start with a envvars.json like this (fill out actual values):
```
{
    "GITHUB_APP_ID": "A six digit number found in your app's general settings",
    "GITHUB_APP_PRIVATE_KEY": "The location of your app's private key .pem file",
    "GITHUB_REPOSITORY": "The name of the Github repository you want your bot to act upon. Must follow the format {username}/{repo-name}. Make sure the app has been added to this repository first!",
    "GITHUB_BRANCH": "The branch where the bot will make its commits. Defaults to 'master.'",
    "GITHUB_BASE_BRANCH": "The base branch of your repo, usually either 'main' or 'master.' This is where pull requests will base from. Defaults to 'master.'"
    "OPENAI_API_KEY": "The API Key used for communicating with OpenAI."
}
```

## References

* [Langchain Github Toolkit Library](https://python.langchain.com/docs/integrations/toolkits/github)
* [Github Application Registration](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps)
* [Github Application Quickstart Guide](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/quickstart)
* [Github Application Code Writing Guide](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/about-writing-code-for-a-github-app)