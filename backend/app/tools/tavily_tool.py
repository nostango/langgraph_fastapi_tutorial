from langchain_community.tools.tavily_search import TavilySearchResults

# This is the tool that will be used by the agent to search the web
# It is initialized with a max_results parameter of 1, which means it will only return the most relevant result.
search_tool = TavilySearchResults(max_results=2)
