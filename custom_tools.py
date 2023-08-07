from langchain.agents import tool
from googlesearch import search

@tool
def search_online(input:str):
    """
    Search Online
    """
    
    result = search(input, num_results=1)

    return result

