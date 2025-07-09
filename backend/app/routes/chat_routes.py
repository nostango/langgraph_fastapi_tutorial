from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.workflows.chat_workflow import get_graph

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def handle_chat_request(request: ChatRequest):
    """
    This endpoint handles a chat request.
    It invokes the LangGraph workflow with the user's message
    and returns the AI's response.
    """
    # Get the compiled graph from the workflow module
    graph = get_graph()

    # Define the configuration for the graph invocation, specifying the session_id
    # This ensures that the conversation state is managed correctly for each user.
    config = {"configurable": {"thread_id": request.session_id}}

    # The graph expects a list of messages. We wrap the user's message
    # in a `HumanMessage` object, which is the standard format.
    input_message = [HumanMessage(content=request.message)]

    # Invoke the graph with the user's messages
    final_state = graph.invoke(
        {"messages": input_message},
        config=config
    )

    # The response from the graph is the last message in the state's message list.
    # This will be an `AIMessage` object.
    ai_response = final_state["messages"][-1]

    return ChatResponse(
        response=ai_response.content, # Extract the string content from the AIMessage
        session_id=request.session_id
    )
