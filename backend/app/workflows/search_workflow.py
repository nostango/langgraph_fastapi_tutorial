from typing import Annotated

from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from app.tools.tavily_tool import search_tool

# This defines the structure of the agent's state.
# It's a dictionary with a single key, "messages", which is a list of messages.
# The `add_messages` function ensures that new messages are appended to the list.
# TODO: Migrate this State from TypedDict to a Pydantic BaseModel for better 
# performance and validation in production.
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the graph, telling it what the structure of its state will be.
graph_builder = StateGraph(State)

# -- Define the nodes and edges of the graph --

# 1. The LLM node
# Initialize the LLM and bind the search tool to it.
# This tells the LLM that it has access to this tool.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools([search_tool])

# This function will be called when the "chatbot" node is executed.
# It invokes the LLM with the current state (messages).
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Add the chatbot node to the graph.
graph_builder.add_node("chatbot", chatbot)

# 2. The Tool node
# This is a pre-built node from LangGraph that executes tools.
# It takes the tool calls from the last message and runs them.
# TODO: Add error handling logic here to manage cases where the search tool 
# fails (e.g., API key issues or no results found).
tool_node = ToolNode(tools=[search_tool])
graph_builder.add_node("tools", tool_node)

# 3. The Conditional Edge
# This is the routing logic. After the "chatbot" node runs, this condition is checked.
# `tools_condition` is a pre-built function that checks if the last message contains tool calls.
# If it does, the graph transitions to the "tools" node.
# If it does not, the graph transitions to the special END node, and execution finishes.
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
# When the graph is invoked, it will always start at the "chatbot" node.
graph_builder.add_edge(START, "chatbot")


# -- Compile the graph --
# This creates the final, runnable agent.
agent_executor = graph_builder.compile()