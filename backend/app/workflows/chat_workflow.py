# 1. Import necessary libraries
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# 2. Import your own modules
from app.schemas.chat_schemas import GraphState
from app.llm.llm_factory import llm # Import the cached LLM instance

# 3. Define the main chatbot workflow

# Initialize the LangGraph StateGraph with our defined state
graph_builder = StateGraph(GraphState)

# The LLM is now imported directly from the factory.
# To change the model, you only need to edit `config.yaml`.

def chatbot(state: GraphState):
    """
    This is the single node in our graph.
    It takes the current conversation state, calls the LLM,
    and returns the LLM's response.
    """
    # TODO: Wrap this invoke in a retry block (e.g., using RunnableRetry) 
    # to handle rate limits or temporary provider outages.
    # The `state.messages` contains the entire conversation history.
    response = llm.invoke(state.messages)
    
    # The `add_messages` helper in our GraphState will automatically
    # append this new response to the list of messages.
    return {"messages": [response]}


# Add the `chatbot` function as a node in the graph.
# We'll name the node "chatbot" as well.
graph_builder.add_node("chatbot", chatbot)

# Set the entry and finish points of the graph.
# For this simple graph, it starts at the chatbot node and ends immediately after.
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")

# Add a memory saver to keep track of the conversation history.
memory = MemorySaver()

# Compile the graph into a runnable object.
# The checkpointer ensures that the state (conversation history) is saved
# between invocations.
graph = graph_builder.compile(checkpointer=memory)

# 4. Create a helper function to expose the graph
def get_graph():
    """
    Returns the compiled LangGraph instance.
    This is a clean way to make the graph accessible to other parts of the application,
    like the API routes, without causing circular import issues.
    """
    return graph
