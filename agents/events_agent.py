# Natural Events Agent - fetches and interprets NASA EONET event data
# Specialist in natural disasters and extreme weather events

from langchain.core.tools import tool
from langchain.ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from tools.nasa_eonet import (
    get_recent_events,
    get_event_statistics,
    format_events_summary,
    format_stats_summary
)

MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """
You are a Natural Events Specialist with access to NASA EONET satellite tracking data.
Your role is to:
- Track active natural events like wildfires, storms, floods, volcanoes
- Analyse patterns in natural disaster frequency
- Explain the significance of current events
- Identify which regions or event types are most active

Always use your tools to fetch real data before answering.
Be factual and specific. Explain events clearly and their potential climate implications.
"""

@tool
def fetch_recent_events(days: int = 30, category: str = None) -> str:
    """
    Fetch recent natural events from NASA EONET satellite tracking.
    Categories include wildfires, severe storms, volcanoes, floods, landslides, sea/lake ice, drought, dust storms, earthquakes, temperature extremes.
    Use None for category to get all events.

    Parameters:
    days (int): How many days back to fetch (default 30)
    category (str, optional): Filter by specific category
    """
    data = get_recent_events(days=days, category=category)
    return format_events_summary(data)

@tool
def fetch_event_statistics(days: int = 90) -> str:
    """
    Fetch count of natural events by category over a time period from NASA EONET.
    Use this to understand which types of events are most frequent.

    Parameters:
    days (int): Analysis period (default 90)
    """
    data = get_event_statistics(days=days)
    return format_stats_summary(data)

def build_events_agent():
    """Build and return the Natural Events Agent."""
    model = ChatOllama(model=MODEL, temperature=0)
    tools = [fetch_recent_events, fetch_event_statistics]
    return create_react_agent(model, tools, prompt=SYSTEM_PROMPT)

def run_events_agent(question: str) -> str:
    """Run the events agent on a question and return its answer."""
    agent = build_events_agent()
    result = agent.invoke({"messages": [("human", question)]})
    return result["messages"][-1].content