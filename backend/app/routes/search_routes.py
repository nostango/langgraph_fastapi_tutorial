from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from app.schemas.search_schemas import SearchRequest, SearchResponse
from app.workflows.search_workflow import agent_executor

router = APIRouter()

@router.post("", response_model=SearchResponse)
async def handle_search_request(request: SearchRequest):
    """
    This endpoint handles a search request.
    It invokes the LangGraph agent with the user's message
    and returns the AI's response.
    """
    try:
        config = {"configurable": {"thread_id": request.session_id}}
        input_message = [HumanMessage(content=request.message)]
        response = agent_executor.invoke({"messages": input_message}, config=config)
        ai_response = response["messages"][-1]

        return SearchResponse(
            response=ai_response.content,
            session_id=request.session_id
        )
    except Exception as e:
        print(f"❌ Error in search route: {str(e)}")
        return SearchResponse(
            response="I was unable to complete the search. Please check your query or try again later.",
            session_id=request.session_id
        )
