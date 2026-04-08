from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

from agents.climate_agent import run_climate_agent
from agents.events_agent import run_events_agent
from agents.weather_agent import run_weather_agent
from agents.analysis_agent import run_analysis_agent

MODEL = "llama3.1:8b"

# ---------------------------
# State
# ---------------------------
class ResearchState(TypedDict):
    question: str
    route: str
    response: str


# ---------------------------
# Router Prompt
# ---------------------------
ROUTER_PROMPT = """
You are a routing assistant for a climate research system.

Classify the user's question into exactly ONE category:

- climate: long-term climate patterns, 30-year averages, historical climate norms
- events: natural disasters, wildfires, storms, floods, volcanoes, earthquakes
- weather: recent weather, current conditions, short-term forecasts
- analysis: multi-source synthesis, comparisons, deep research

Reply with ONLY ONE WORD from:
climate, events, weather, analysis
"""


# ---------------------------
# Router Node
# ---------------------------
def route_question(state: ResearchState) -> ResearchState:
    model = ChatOllama(model=MODEL, temperature=0)

    messages = [
        SystemMessage(content=ROUTER_PROMPT),
        HumanMessage(content=f"Question: {state['question']}\n\nCategory:")
    ]

    response = model.invoke(messages)

    raw = response.content.strip().lower()
    first_word = raw.split()[0] if raw else "analysis"

    valid = {"climate", "events", "weather", "analysis"}
    route = first_word if first_word in valid else "analysis"

    print(f"\n[Router] → {route}")

    return {**state, "route": route}


# ---------------------------
# Agent Nodes
# ---------------------------
def climate_node(state: ResearchState) -> ResearchState:
    print("[Agent] Climate Specialist")
    response = run_climate_agent(state["question"])
    return {**state, "response": response}


def events_node(state: ResearchState) -> ResearchState:
    print("[Agent] Events Specialist")
    response = run_events_agent(state["question"])
    return {**state, "response": response}


def weather_node(state: ResearchState) -> ResearchState:
    print("[Agent] Weather Specialist")
    response = run_weather_agent(state["question"])
    return {**state, "response": response}


def analysis_node(state: ResearchState) -> ResearchState:
    print("[Agent] Senior Analyst")
    response = run_analysis_agent(state["question"])
    return {**state, "response": response}


# ---------------------------
# Conditional Router
# ---------------------------
def choose_agent(state: ResearchState) -> str:
    return state["route"]


# ---------------------------
# Build Graph
# ---------------------------
def build_orchestrator():
    graph = StateGraph(ResearchState)

    # Nodes
    graph.add_node("router", route_question)
    graph.add_node("climate", climate_node)
    graph.add_node("events", events_node)
    graph.add_node("weather", weather_node)
    graph.add_node("analysis", analysis_node)

    # Entry
    graph.add_edge(START, "router")

    # Router → specialist
    graph.add_conditional_edges(
        "router",
        choose_agent,
        {
            "climate": "climate",
            "events": "events",
            "weather": "weather",
            "analysis": "analysis",
        },
    )

    # Specialists → END
    graph.add_edge("climate", END)
    graph.add_edge("events", END)
    graph.add_edge("weather", END)
    graph.add_edge("analysis", END)

    return graph.compile()


# ---------------------------
# Singleton
# ---------------------------
_orchestrator = None


def get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = build_orchestrator()
    return _orchestrator


# ---------------------------
# Public API
# ---------------------------
def run_research(question: str) -> dict:
    orchestrator = get_orchestrator()

    initial_state: ResearchState = {
        "question": question,
        "route": "",
        "response": "",
    }

    result = orchestrator.invoke(initial_state)
    return result


# ---------------------------
# CLI Entry
# ---------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
    else:
        q = input("Climate Research Question: ").strip()

    print(f"\nQuestion: {q}\n{'='*60}")

    result = run_research(q)

    print(f"\n{'='*60}")
    print(f"Agent: {result['route'].upper()} SPECIALIST")
    print(f"{'='*60}\n")

    print(result["response"])