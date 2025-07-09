# This main file is the entry point for the application in its entirety

# 1. Load environment variables before anything else.
# This ensures that all modules have access to the necessary secrets.
from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI
from app.routes import chat_routes, mcp_routes # Import both routers

# Create the FastAPI instance, this is how you use and implement FastAPI
app = FastAPI(
    title="Template for advanced LLM applications",
    description="This is a template for advanced LLM applications",
    version="0.1.0"
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the LLM App API!"}

# Include the router for our own frontend (the "Lightning port")
app.include_router(chat_routes.router, prefix="/chat", tags=["chat"])

# Include the router for external clients (the "USB-C port")
app.include_router(mcp_routes.router, prefix="/mcp", tags=["mcp"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
