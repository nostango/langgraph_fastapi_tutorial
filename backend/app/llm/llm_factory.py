from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint

from app.config.core import config

def get_llm(callbacks=None):
    """
    Factory function to initialize the LLM based on config.yaml.
    Supports global callbacks for observability (e.g., LangSmith).
    """
    llm_config = config['llm']
    provider = llm_config.get("provider")
    model_name = llm_config.get("model_name")
    model_params = llm_config.get("config", {})

    # Ensure callbacks is at least an empty list if not provided
    if callbacks is None:
        callbacks = []

    # --- Global Observability ---
    # In 2025-2026, LangSmith tracing is typically handled by env vars, 
    # but we can explicitly add handlers here if we want custom logic
    # or secondary logging (e.g., to a local file or custom dashboard).

    if provider == "openai":
        return ChatOpenAI(
            model=model_name, 
            callbacks=callbacks,
            **model_params
        )
    
    elif provider == "huggingface":
        return HuggingFaceEndpoint(
            repo_id=model_name, 
            callbacks=callbacks,
            **model_params
        )
    
    elif provider == "lmstudio":
        # LM Studio provides an OpenAI-compatible API locally.
        # Default local URL is http://localhost:1234/v1
        base_url = model_params.pop("base_url", "http://localhost:1234/v1")
        return ChatOpenAI(
            model=model_name,
            base_url=base_url,
            api_key="lm-studio", # LM Studio doesn't require a real key
            callbacks=callbacks,
            **model_params
        )

    # --- Add other providers here ---
    # elif provider == "anthropic":
    #     return ChatAnthropic(model=model_name, **model_params)

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Please check config.yaml.")

llm = get_llm()
