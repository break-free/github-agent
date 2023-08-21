import os
from langchain.agents import tool
from googlesearch import search
from github import Github
from github import Auth

@tool
def create_new_tool(tool_name:str):
    """
    Create a new tool if you cannot find tools to meet the request.
    """

    functionTemplate = f"""
    @tool
    \"\"\"
    Your new tool {tool_name}, created by an agent!
    \"\"\"
    def create_new_tool({tool_name}:str):
    string = "This is your new tool"

        return string
    """

    with open("custom_tools.py", "+a") as f:
        f.write(functionTemplate)

    return f"Wrote the following code: {functionTemplate}"