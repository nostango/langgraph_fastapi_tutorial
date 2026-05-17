from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint

from app.config.core import config

def get_llm():
    # TODO: Add global callback handlers here for LangSmith tracing 
    # so every LLM call across all workflows is automatically logged.
    llm_config = config['llm']
    provider = llm_config.get("provider")
    model_name = llm_config.get("model_name")
    model_params = llm_config.get("config", {})

    if provider == "openai":
        return ChatOpenAI(model=model_name, **model_params)
    
    elif provider == "huggingface":
        return HuggingFaceEndpoint(repo_id=model_name, **model_params)

    # --- Add other providers here ---
    # elif provider == "anthropic":
    #     return ChatAnthropic(model=model_name, **model_params)

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Please check config.yaml.")

llm = get_llm()
