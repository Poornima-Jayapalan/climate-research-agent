# Climate Data Agent - fetches and interprets NASA POWER climate data
# Specialist in long-term climate patterns and temperature trends

from langchain.core.tools import tool
from langchain.ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from tools.nasa_power import (
    get_climate_data,
    get_temperature_trend,
    format_climate_summary,
    format_trend_summary
)

MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """
You are a Climate Data Specialist with access to NASA POWER satellite data.
Your role is to:
- Fetch and interpret long-term climate patterns for any location
- Analyse temperature trends over time
- Explain what the data means in plain language
- Identify warming or cooling trends

Always use your tools to fetch real data before answering.
Be specific with numbers. Explain climate patterns clearly for a non-expert audience.
"""

@tool
def fetch_climate_data(lat: float, lon: float) -> str:
    """
    Fetch 30-year average climate data for a location from NASA POWER.
    Includes temperature, precipitation, wind speed, solar radiation.
    
    Parameters:
    lat (float): Latitude
    lon (float): Longitude
    """
    data = get_climate_data(lat, lon)
    return format_climate_summary(data)

@tool
def fetch_temperature_trend(lat: float, lon: float, start_year: int, end_year: int) -> str:
    """
    Fetch annual temperature data for a location over a range of years from NASA POWER.
    Use this to analyse whether a location is warming or cooling over time.
    
    Parameters:
    lat (float): Latitude
    lon (float): Longitude
    start_year (int): Start year (e.g., 2000)
    end_year (int): End year (e.g., 2023)
    """
    data = get_temperature_trend(lat, lon, start_year, end_year)
    return format_trend_summary(data)

def build_climate_agent():
    """Build and return the Climate Data Agent."""
    model = ChatOllama(model=MODEL, temperature=0)
    tools = [fetch_climate_data, fetch_temperature_trend]
    return create_react_agent(model, tools, prompt=SYSTEM_PROMPT)

def run_climate_agent(question: str) -> str:
    """Run the climate agent on a question and return its answer."""
    agent = build_climate_agent()
    result = agent.invoke({"messages": [("human", question)]})
    return result["messages"][-1].content