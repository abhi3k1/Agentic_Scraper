Agentic Scraper — LangChain Production Agent
==========================================

Overview
--------
This project provides a production-ready scaffold for an agentic web-scraping
service built with LangChain and FastAPI. It implements the core toolset
(fetch, parse, extract), a LangChain agent wrapper, simple persistence using
SQLite, and an HTTP API to submit scraping jobs.

Quick start
-----------
1. Create a Python environment (3.10+)

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy environment variables

```bash
cp .env.example .env
# Edit .env to set GOOGLE_APPLICATION_CREDENTIALS (or other provider keys)
```

3. Run the service

```bash
uvicorn agent.app:app --host 0.0.0.0 --port 8000
```

Usage
-----
POST /scrape

JSON body:

```
{
  "url": "https://example.com/product/1",
  "selectors": {"title": "h1", "price": ".price"}
}
```

Response: JSON with `data` (dictionary of extracted fields), `status`, and
`id` (database id).

Production notes
----------------
- Use environment variables to configure LLM provider and model.
- Run behind an autoscaling API gateway; use a task queue (Redis/RQ/Celery)
  for large jobs.
- Add LangSmith or equivalent tracing for observability.

Files of interest
- `src/agent/app.py` — FastAPI application and endpoints
- `src/agent/agent_core.py` — LangChain agent initialization and tool wiring
- `src/agent/tools/*` — fetch/parse/extract tools
- `src/agent/storage/database.py` — SQLite persistence
