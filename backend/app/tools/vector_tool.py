from langchain_core.tools import tool
from app.utils.vector_store import query_vector_store

# TODO: Define the @tool that the LLM will actually see.
# 1. Write a very clear docstring - this is the "prompt" for the LLM.
# 2. Call the `query_vector_store` function from your utils.
# 3. Handle potential errors (e.g., database is down).

@tool
def search_knowledge_base(query: str) -> str:
    """
    Add a descriptive docstring here. 
    Example: 'Useful for searching the company's internal documentation about [Topic X].'
    """
    return query_vector_store(query)
