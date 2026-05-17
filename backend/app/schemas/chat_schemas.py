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

# TODO: Migrate this from TypedDict to a Pydantic BaseModel (v2/v3).
# Pydantic states provide 5-10x better performance and built-in validation
# for every node transition, which is the 2026 standard for production agents.
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
