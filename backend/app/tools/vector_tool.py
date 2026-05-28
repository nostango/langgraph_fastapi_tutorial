from langchain_core.tools import tool
from app.utils.vector_store import query_vector_store

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the company's internal documentation for specific technical info, 
    architecture standards, and best practices. Use this tool when the user 
    asks about internal guidelines or specific project structures.
    """
    try:
        return query_vector_store(query)
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"
