# This file defines the standard data contracts for the Model Context Protocol (MCP).
# These are generic blueprints for how any MCP-compliant tool should communicate with our service.

from pydantic import BaseModel, Field
from typing import Dict, Any

class MCPRequest(BaseModel):
    """
    A standard request from any external MCP client.
    """
    # Defines the action the client wants to perform, e.g., "chat", "summarize".
    action: str = Field(..., description="The action to be performed by the workflow.")
    
    # A flexible payload containing the data needed for the action.
    # For a "chat" action, this might be {"message": "Hello"}.
    payload: Dict[str, Any] = Field(..., description="A dictionary containing the data for the action.")
    
    # A session ID to maintain context across requests.
    session_id: str = Field(..., description="A unique identifier for the conversation thread.")

class MCPResponse(BaseModel):
    """
    A standard response sent back to any MCP client.
    """
    # Indicates the status of the request processing.
    status: str = "success"
    
    # A flexible payload containing the result of the action.
    # For a "chat" action, this might be {"response": "Hi there!"}.
    data: Dict[str, Any]
