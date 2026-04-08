#  Multi-Agent Climate Research 

A multi-agent AI system for climate research, powered by real-world data from NASA and Open-Meteo. Ask any climate, weather, or natural events question in plain language and get data-backed answers from a specialist AI agent.

---

##  Overview

This project uses a **LangGraph orchestrator** to route user questions to the most appropriate specialist agent.

Each agent:

* Fetches live data from free public APIs
* Uses a local LLM (via Ollama) to interpret and explain results

###  Workflow

1. User asks a question
2. Router (Llama 3.1:8b) classifies it
3. Routed to the correct specialist agent:

   * Climate
   * Events
   * Weather
   * Analysis

---

## Features

* **Intelligent routing** – Questions automatically sent to the right agent
* **4 specialist agents** – Each with purpose-built tools and prompts
* **3 free data sources** – No API keys required
* **Runs locally** – No cloud AI costs
* **Streamlit UI** – Clean browser interface with chat history
* **CLI mode** – Run queries directly from terminal

---

##  Agents

| Agent                     | Specialty                              | Data Source |
| ------------------------- | -------------------------------------- | ----------- |
| Climate Data Specialist   | Long-term trends, 30-year averages     | NASA POWER  |
| Natural Events Specialist | Wildfires, floods, storms, earthquakes | NASA EONET  |
| Weather Specialist        | Current + historical weather           | Open-Meteo  |
| Senior Climate Analyst    | Multi-source synthesis & comparisons   | All sources |

---

##  Data Sources

| API        | What it Provides                               | Cost |
| ---------- | ---------------------------------------------- | ---- |
| NASA POWER | Meteorological & climatological satellite data | Free |
| NASA EONET | Real-time natural event tracking               | Free |
| Open-Meteo | Forecasts & historical weather                 | Free |

---

##  Tech Stack

| Component     | Technology  |
| ------------- | ----------- |
| Orchestration | LangGraph   |
| LLM Framework | LangChain   |
| LLM Runtime   | Ollama      |
| LLM Model     | llama3.1:8b |
| UI            | Streamlit   |

---

##  Requirements

* Python 3.10
* Ollama installed and running
* Llama3.1:8b model pulled locally

---

##  Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd climate-research-agent
```

### 2. Create and activate a virtual environment

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 📥 Setup

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull the LLM model via Ollama

```bash
ollama pull llama3.1:8b
```

Make sure the Ollama service is running before launching the app.

---

##  Usage

### Run Streamlit app

```bash
streamlit run app.py
```

Then open your browser at:

```
http://localhost:8501
```

---

###  CLI Usage

Run a single query:

```bash
python orchestrator.py "What is the climate like in Sydney, Australia?"
```

Or run interactively:

```bash
python orchestrator.py
```

---

##  Example Questions

* What is the climate like in Sydney, Australia?
* Are there any active wildfires in the past 30 days?
* What is the current weather in London?
* Has Delhi been warming over the past 20 years?
* Compare the weather in New York this January vs last January
* What natural events have been most frequent this year?
* Give me a comprehensive climate analysis of Cape Town

---

##  Project Structure

```
climate-research-agent/
│
├── app.py                 # Streamlit UI
├── orchestrator.py        # LangGraph router and workflow
├── requirements.txt
│
├── agents/
│   ├── climate_agent.py   # NASA POWER (climate trends)
│   ├── events_agent.py    # NASA EONET (natural disasters)
│   ├── weather_agent.py   # Open-Meteo (weather data)
│   └── analyst_agent.py   # Multi-source analysis
│
└── tools/
    ├── nasa_power.py
    ├── nasa_eonet.py
    └── open_meteo.py
```

---

##  License

MIT License

---

##  Notes

* Runs fully locally using Ollama
* No API keys required
* Ideal for experimentation with multi-agent systems and climate data

---
