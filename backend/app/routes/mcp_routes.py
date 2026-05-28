# --- Protocol Engineering: Official MCP Server Implementation ---
from mcp.server.fastmcp import FastMCP
from app.workflows.chat_workflow import get_graph
from langchain_core.messages import HumanMessage

# 1. Initialize FastMCP
# This handles the JSON-RPC 2.0 handshake and capability negotiation automatically.
mcp = FastMCP("AgenticHub")

# 2. Define Tools (The Meta-Tool Pattern)
# Instead of hardcoding every workflow, we expose a standard interface 
# that external agents can discover and use.

@mcp.tool()
async def chat_with_agent(message: str, session_id: str = "default") -> str:
    """
    Primary tool to interact with the internal LangGraph chat agent.
    Use this for general conversation and stateful interactions.
    """
    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}
    input_messages = [HumanMessage(content=message)]
    
    # Invoke the graph (In production, you'd add the RequestResponder patch here)
    final_state = graph.invoke(
        {"messages": input_messages},
        config=config
    )
    
    return final_state.messages[-1].content

# 3. Dynamic Discovery (Coming Soon)
# @mcp.tool()
# def list_available_workflows():
#     """Returns a directory of all specialized agent workflows available in this hub."""
#     return ["chat", "search"]

# 4. Security & Compatibility
# Note: For macOS + Python 3.12/3.13, we use SSE transport via the FastAPI mount.
