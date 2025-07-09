# This file implements the MCP endpoint.
# It acts as a universal adapter, translating standard MCP requests
# into the format our internal workflows understand.

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage

# Import the standard MCP schemas and our internal workflow
from app.schemas.mcp_schemas import MCPRequest, MCPResponse
from app.workflows.chat_workflow import get_graph

router = APIRouter()

@router.post("/invoke", response_model=MCPResponse)
async def handle_mcp_invoke(request: MCPRequest):
    """
    This is the universal MCP endpoint.
    It can handle different actions by routing them to the appropriate workflow.
    """
    # 1. Check which action the external client wants to perform.
    if request.action == "chat":
        # 2. If it's a chat action, get our compiled chat graph.
        graph = get_graph()
        
        # 3. Translate the generic MCP payload into the specific format
        #    our chat workflow expects.
        message_content = request.payload.get("message")
        if not message_content:
            raise HTTPException(status_code=400, detail="Payload for 'chat' action must contain a 'message' field.")
        
        # Our workflow expects a list of LangChain message objects.
        input_messages = [HumanMessage(content=message_content)]
        
        # 4. Prepare the config for the graph invocation, using the MCP session_id.
        config = {"configurable": {"thread_id": request.session_id}}
        
        # 5. Invoke the graph.
        final_state = graph.invoke(
            {"messages": input_messages},
            config=config
        )
        
        # 6. Translate the internal result back into the standard MCP response format.
        ai_response = final_state["messages"][-1]
        response_data = {"response": ai_response.content}
        
        return MCPResponse(data=response_data)

    # --- You could add other actions here ---
    # elif request.action == "summarize":
    #     # ... call a summarization workflow ...
    #     pass

    else:
        # If the action is not supported, return an error.
        raise HTTPException(status_code=400, detail=f"Unsupported action: {request.action}")
