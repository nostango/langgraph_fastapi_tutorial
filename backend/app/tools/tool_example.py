from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional

# --- Tool Input Schema (Pydantic v2) ---

class WeatherInput(BaseModel):
    """Input for the weather tool."""
    location: str = Field(description="The city and state, e.g. San Francisco, CA")
    unit: Optional[str] = Field(default="celsius", description="The unit of temperature (celsius or fahrenheit)")

# --- Tool Definition ---

@tool(args_schema=WeatherInput)
def get_current_weather(location: str, unit: str = "celsius") -> str:
    """
    Get the current weather in a given location.
    Use this tool whenever a user asks about the weather or temperature.
    """
    # 1. API Connection (Logic)
    # In a real app, you would use `os.getenv("WEATHER_API_KEY")` here.
    # api_key = "your_api_key_here"
    
    # 2. Execution
    print(f"🌡️ Fetching weather for {location} in {unit}...")
    
    # Simulating an API response
    return f"The weather in {location} is currently 22 degrees {unit} and sunny."

# --- Usage Instructions ---
# To use this tool in a workflow:
# 1. Import it: `from app.tools.tool_example import get_current_weather`
# 2. Bind it to the LLM: `llm.bind_tools([get_current_weather])`
# 3. Add it to the ToolNode: `ToolNode(tools=[get_current_weather])`
