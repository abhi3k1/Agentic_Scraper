# Agentic Scraper (LangChain) — AI scraping agent

Overview
- FastAPI service that fetches webpages and extracts structured fields using `extractor` utilities. Includes a small LangChain agent builder in `agent_core.py` for advanced workflows.

Quick run (development)
- Create a Python 3.10+ venv and install requirements.

Commands:
```powershell
cd Agentic_Scraper_LangChain
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.agent.app:app --reload --port 8000
```

API
- `POST /scrape` — body: `{ "url": "https://...", "selectors": {"title":"css selector"} }` -> returns extracted fields and stores the extraction.

Integration
- The agent writes minimal extraction records to its local DB. The backend can poll or accept posted extraction payloads.

Notes
- Configure LLM provider via `src/agent/config.py` if using the LangChain agent.
