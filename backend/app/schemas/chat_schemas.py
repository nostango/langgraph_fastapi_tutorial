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


# --- Workflow State Model (TypedDict) ---

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
