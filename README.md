# Plug-and-Play Agentic Template

This is a template for building LLM-powered applications using **LangGraph**, **FastAPI**, that is hooked up to a **Next.js** frontend for testing/demonstration. 

The goal of this is to have a template for agentic workflows where you can drop in custom logic for a client and plug it in anywhere

---

## What are you looking at? (The 3 Pillars)

When you need to customize this for a specific job (like a "CSV Analyzer" or a "Document Generator"), you only need to focus on these three things:

### 1. The Workflows (`backend/app/workflows/`)
*   **The Brain:** This is your "Composer." You use LangGraph to string together nodes (logical steps) and edges (the paths between them).
*   **Customization:** Need a new step? Add a node. Need to change how the agent thinks? Edit the graph here.

### 2. The Tools (`backend/app/tools/`)
*   **The Hands:** These are the specific actions your agent can take (e.g., searching Tavily, querying a Postgres database, or reading a local file).
*   **Customization:** Define your functions here, wrap them in the `@tool` decorator, and bind them to your LLM in the workflow.

### 3. The Schemas (`backend/app/schemas/`)
*   **The Rules:** This is the "Data Contract" for your app.
*   **API Schemas:** Define what the user sends from the frontend.
*   **Graph State:** Define what the agent "remembers" as it moves between nodes.

---

## The Flow: FastAPI + LangGraph

How does a message actually turn into an answer?

1.  **The Route:** A user sends a request to a FastAPI endpoint (like `/chat` or `/search`).
2.  **The Hand-off:** The route calls `graph.invoke()`. This kicks off the LangGraph engine.
3.  **The Logic:** LangGraph moves through your nodes. It might call a **Tool** to look something up, update its **State** with what it found, and then ask the **LLM** to write the final response.
4.  **The Return:** Once the graph hits the `END` node, the final state is sent back through the FastAPI route as a JSON response.

---

## The Frontend (Next.js)

The `/frontend` folder is a **Next.js 15** application. 

*   **Connection:** It is designed to talk to the FastAPI backend (defaulting to `http://localhost:8000`).
*   **Usage:** To see the app in action, run the backend server first, then navigate to the frontend folder and run `npm run dev`. 
*   **Note:** Current frontend is a clean scaffold. You can build your custom chat interface in `src/app/page.tsx` and point your `fetch` calls to the FastAPI routes.

---

## How to use this for a new job

1.  **Define your Schema:** What does the user need to send? (Add to `schemas/`).
2.  **Build your Tools:** What data does the agent need to access? (Add to `tools/`).
3.  **Compose your Workflow:** How should the agent use those tools? (Add to `workflows/`).
4.  **Expose the Route:** Make a new endpoint in `routes/` so the frontend can trigger your new workflow.

