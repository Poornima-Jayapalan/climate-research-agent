# Weather Agent - fetches historical and current weather from Open-Meteo
# Specialist in short-term weather patterns and recent conditions

from langchain.core.tools import tool
from langchain.ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from tools.open_meteo import (
    get_historical_climate,
    get_recent_weather,
    format_historical_summary
)

MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """
You are a Weather Data Specialist with access to Open-Meteo historical and forecast data.
Your role is to:
- Fetch historical weather data for any location and date range
- Retrieve current and forecast weather conditions
- Identify unusual weather patterns or anomalies
- Compare recent weather to historical norms

Always use your tools to fetch real data before answering.
Be specific with numbers and dates. Explain weather patterns clearly.
"""

@tool
def fetch_historical_weather(lat: float, lon: float, start_date: str, end_date: str) -> str:
    """
    Fetch historical daily weather data from Open-Meteo for a location and date range.
    Use for questions about past weather conditions.

    Parameters:
    lat (float): Latitude
    lon (float): Longitude
    start_date (str): Start date in YYYY-MM-DD format
    end_date (str): End date in YYYY-MM-DD format
    """
    data = get_historical_climate(lat, lon, start_date, end_date)
    return format_historical_summary(data)

@tool
def fetch_current_weather(lat: float, lon: float) -> str:
    """
    Fetch current weather and 7-day forecast from Open-Meteo for a location.
    Use for questions about current or upcoming weather conditions.

    Parameters:
    lat (float): Latitude
    lon (float): Longitude
    """
    data = get_recent_weather(lat, lon, days=7)
    if "error" in data:
        return f"Open-Meteo error: {data['error']}"

    lines = [
        f"Current Weather at ({lat}, {lon})",
        f"Source: {data.get('source', 'Unknown')}",
        f"Current temperature: {data.get('current_temp_c', 'N/A')} °C",
        f"Current wind speed: {data.get('current_wind_ms', 'N/A')} m/s",
        "7-day forecast:"
    ]

    for day in data.get("forecast", []):
        lines.append(
            f"{day['date']}: Max {day.get('temp_max_c', 'N/A')} °C, "
            f"Min {day.get('temp_min_c', 'N/A')} °C, "
            f"Precipitation {day.get('precip_mm', 'N/A')} mm"
        )

    return "\n".join(lines)

def build_weather_agent():
    """Build and return the Weather Agent."""
    model = ChatOllama(model=MODEL, temperature=0)
    tools = [fetch_historical_weather, fetch_current_weather]
    return create_react_agent(model, tools, prompt=SYSTEM_PROMPT)

def run_weather_agent(question: str) -> str:
    """Run the weather agent on a question and return its answer."""
    agent = build_weather_agent()
    result = agent.invoke({"messages": [("human", question)]})
    return result["messages"][-1].content