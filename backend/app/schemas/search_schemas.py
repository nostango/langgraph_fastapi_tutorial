from pydantic import BaseModel

class SearchRequest(BaseModel):
    message: str
    session_id: str

class SearchResponse(BaseModel):
    response: str
    session_id: str
