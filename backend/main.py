# This main file is the entry point for the application in its entirety

# 1. Load environment variables before anything else.
# This ensures that all modules have access to the necessary secrets.
from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat_routes, mcp_routes, search_routes 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    # This is the "Pro" way to handle initialization (Tracing, DB pools, etc.)
    print("🚀 Starting up Agentic API...")
    print("📈 Observability: LangSmith Tracing ready (checking .env...)")
    yield
    # --- Shutdown Logic ---
    print("🛑 Shutting down Agentic API...")

# Create the FastAPI instance
app = FastAPI(
    title="Template for advanced LLM applications",
    description="This is a template for advanced LLM applications",
    version="0.1.0",
    lifespan=lifespan
)

# --- Universal Access (CORS) ---
# This allows your API to be plugged into Next.js or any other frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the LLM App API!"}

# Include the router for our own frontend
app.include_router(chat_routes.router, prefix="/chat", tags=["chat"])

# Include the router for external clients
# TODO: Once migrated to FastMCP, mount the SSE app here using:
# app.mount("/mcp", mcp.sse_app()) 
# This replaces the manual router for full protocol compliance.
app.include_router(mcp_routes.router, prefix="/mcp", tags=["mcp"])

# Include the new search router
app.include_router(search_routes.router, prefix="/search", tags=["search"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
