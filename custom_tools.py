import os
from langchain.agents import tool
from googlesearch import search
from git import Repo

@tool
def search_online(input:str):
    """
    Search online for and return the very first link found from an input term or phrase.
    """
    
    # Just a limitation of the package used; if you don't use a list it'll provide a generator class instead of a string:
    result = list(search(term=input, num_results=1))
        
    return result[0]

@tool
def create_branch(new_branch:str):
    """
    Create a new git branch from the provided repository
    """

    curr_dir = os.path.dirname(os.path.realpath(__file__))
    repo = Repo(curr_dir)

    current = repo.create_head(new_branch)
    current.checkout()
    main = self.repo.heads.main

create_branch("hello")

