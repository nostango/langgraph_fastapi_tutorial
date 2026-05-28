from typing import Annotated, List
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from app.llm.llm_factory import llm # Use the centralized factory
from app.tools.tavily_tool import search_tool
from app.tools.vector_tool import search_knowledge_base

# This defines the structure of the agent's state.
# Using Pydantic BaseModel provides runtime validation and 
# better integration with production standards.
class State(BaseModel):
    messages: Annotated[List, add_messages] = Field(
        default_factory=list,
        description="The conversation history of the agent."
    )

# Initialize the graph, telling it what the structure of its state will be.
graph_builder = StateGraph(State)

# -- Define the nodes and edges of the graph --

# 1. The LLM node
# Initialize the LLM with retries and bind the search tools.
llm_with_retry = llm.with_retry(stop_after_attempt=3)
llm_with_tools = llm_with_retry.bind_tools([search_tool, search_knowledge_base])

# This function will be called when the "chatbot" node is executed.
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state.messages)]}

# Add the chatbot node to the graph.
graph_builder.add_node("chatbot", chatbot)

# 2. The Tool node
# This is a pre-built node from LangGraph that executes tools.
tool_node = ToolNode(tools=[search_tool, search_knowledge_base])
graph_builder.add_node("tools", tool_node)

# 3. The Conditional Edge
# This is the routing logic. After the "chatbot" node runs, this condition is checked.
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# 4. The Tool-to-Chatbot Edge
# After the "tools" node runs, we always want to go back to the "chatbot" node
# so the LLM can process the tool's output.
graph_builder.add_edge("tools", "chatbot")

# 5. The Start Edge
# This defines the entry point of the graph.
graph_builder.add_edge(START, "chatbot")

# -- Compile the graph --
# This creates the final, runnable agent.
agent_executor = graph_builder.compile()
