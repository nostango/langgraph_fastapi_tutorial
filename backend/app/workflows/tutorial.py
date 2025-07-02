from typing import Annotated, TypedDict
import os

from dotenv import load_dotenv
from langchain_huggingface.llms.huggingface_endpoint import HuggingFaceEndpoint
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_huggingface import HuggingFaceHub

# Load environment variables from .env file
load_dotenv()
api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

hf_llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",   # A known working model :contentReference[oaicite:2]{index=2}
    model_kwargs={"temperature": 0.7, "max_new_tokens": 512}
)


class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):
    # Invoke HF endpoint just like any LLM Runnable
    return {"messages": [hf_llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(user_input)
