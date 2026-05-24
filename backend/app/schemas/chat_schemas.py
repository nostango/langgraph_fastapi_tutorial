from pydantic import BaseModel
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# --- API Data Models (Pydantic) ---

class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    response: str
    session_id: str


# --- Workflow State Model (Pydantic) ---

from typing import List

class GraphState(BaseModel):
    """
    Changed from Dictionary to Pydantic so that:
    1: we are building for FastMCP to be able to read it no problem
    2: we are validating the entry right when we recieve it instead of validating once the data is already inside/not validating and having it break mid process and have to look for the debug
    """
    messages: Annotated[List, add_messages] = Field(
        default_factory=list,
        description="The conversation history of the agent."
    )
