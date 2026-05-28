from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
import json
import asyncio

from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.workflows.chat_workflow import get_graph

router = APIRouter()

async def stream_generator(message: str, session_id: str):
    """
    Generator function that invokes the LangGraph and yields events
    in a format suitable for Server-Sent Events (SSE).
    """
    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}
    input_message = [HumanMessage(content=message)]

    # We use astream_events to get granular updates (tokens, node starts, etc.)
    async for event in graph.astream_events(
        {"messages": input_message},
        config=config,
        version="v2"
    ):
        kind = event["event"]
        
        # We specifically want to stream the tokens from the chat model
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Yield the token in SSE format
                yield f"data: {json.dumps({'type': 'token', 'content': content})}\n\n"
        
        elif kind == "on_chain_end" and event["name"] == "LangGraph":
            # Signal that the entire process is complete
            yield f"data: {json.dumps({'type': 'end'})}\n\n"

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming endpoint for real-time AI responses.
    """
    return StreamingResponse(
        stream_generator(request.message, request.session_id),
        media_type="text/event-stream"
    )

@router.post("", response_model=ChatResponse)
async def handle_chat_request(request: ChatRequest):
    """
    This endpoint handles a chat request.
    It invokes the LangGraph workflow with the user's message
    and returns the AI's response.
    """
    # TODO: Implement a streaming version of this route using `astream_events` 
    # to provide a "live typing" experience on the frontend.
    
    try:
        # Get the compiled graph from the workflow module
        graph = get_graph()

        # Define the configuration for the graph invocation, specifying the session_id
        config = {"configurable": {"thread_id": request.session_id}}

        # The graph expects a list of messages.
        input_message = [HumanMessage(content=request.message)]

        # Invoke the graph with the user's messages
        final_state = graph.invoke(
            {"messages": input_message},
            config=config
        )

        # The response from the graph is the last message in the state's message list.
        ai_response = final_state.messages[-1]

        return ChatResponse(
            response=ai_response.content,
            session_id=request.session_id
        )
    
    except Exception as e:
        # In production, you would log the full traceback to LangSmith
        # and return a clean error message to the user.
        print(f"❌ Error in chat route: {str(e)}")
        return ChatResponse(
            response="I'm sorry, I encountered an error processing your request. Please try again later.",
            session_id=request.session_id
        )
