import streamlit as st
from orchestrator import run_research

# Page config
st.set_page_config(
    page_title="Climate Research Agent",
    page_icon="🌍",
    layout="wide",
)

# Header
st.title("🌍 Climate Research Agent")
st.markdown(
    "A multi-agent AI system powered by **NASA POWER**, **NASA EONET**, and **Open-Meteo** data.\n"
    "Ask any climate, weather, or natural events question."
)

st.divider()

# Sidebar
with st.sidebar:
    st.header("About")

    st.markdown(
        """
        **Agents available:**
        - **Climate** — 30-year averages, long-term patterns  
        - **Events** — Wildfires, storms, floods, volcanoes  
        - **Weather** — Current conditions, forecasts  
        - **Analysis** — Multi-source synthesis  

        **Data sources (all free):**
        - NASA POWER API  
        - NASA EONET API  
        - Open-Meteo API  

        **Model:** llama3.1:8b (local via Ollama)
        """
    )

    st.divider()

    st.header("Example Questions")

    examples = [
        "What is the climate like in Sydney, Australia?",
        "Are there any active wildfires in the past 30 days?",
        "What is the current weather in London?",
        "Has Delhi been warming over the past 20 years?",
        "Compare the weather in New York this January vs last January.",
        "What natural events have been most frequent this year?",
        "Give me a comprehensive climate analysis of Cape Town.",
    ]

    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state["prefill"] = ex

# Session state
if "history" not in st.session_state:
    st.session_state["history"] = []

if "prefill" not in st.session_state:
    st.session_state["prefill"] = ""

# Input
question = st.text_area(
    "Enter your research question:",
    value=st.session_state.get("prefill", ""),
    height=100,
    placeholder="e.g. What is the temperature trend for Mumbai over the last 20 years?",
)

# Clear prefill after use
if st.session_state.get("prefill"):
    st.session_state["prefill"] = ""

# Buttons
col1, col2 = st.columns([1, 5])

with col1:
    run_btn = st.button("Research", type="primary", use_container_width=True)

with col2:
    clear_btn = st.button("Clear History")

if clear_btn:
    st.session_state["history"] = []
    st.rerun()

# Agent labels
AGENT_LABELS = {
    "climate": ("🌡️", "Climate Data Specialist", "blue"),
    "events": ("🔥", "Natural Events Specialist", "orange"),
    "weather": ("🌦️", "Weather Specialist", "green"),
    "analysis": ("📊", "Senior Climate Analyst", "violet"),
}

# Run agent
if run_btn and question.strip():
    with st.spinner("Routing question to specialist agent..."):
        try:
            result = run_research(question.strip())

            st.session_state["history"].insert(
                0,
                (result["question"], result["route"], result["response"]),
            )

        except Exception as e:
            st.error(f"Error: {e}")

# Display history
if st.session_state["history"]:
    st.divider()

    for i, (q, route, resp) in enumerate(st.session_state["history"]):
        icon, label, color = AGENT_LABELS.get(route, ("🤖", "Agent", "grey"))

        with st.expander(
            f"{icon} {q[:80]}{'...' if len(q) > 80 else ''}",
            expanded=(i == 0),
        ):
            st.markdown(f"**Handled by:** :{color}[{icon} {label}]")
            st.divider()
            st.markdown(resp)

else:
    st.info("Ask a question above to start your climate research.")