# Agentic Scraper (LangChain)

A small, extensible web-scraping microservice and LangChain agent that fetches pages, extracts fields via CSS selectors, and stores the results in SQLite. The repository provides a FastAPI HTTP endpoint for direct scraping requests and a LangChain agent with two tools (fetch + extract) that can be used by an LLM to orchestrate scraping tasks.

**Status:** Lightweight demo / starter kit — production hardening required for scale, auth, rate-limiting, and crawling politeness.

---

**Contents**
- What it is
- Architecture & key components
- Quickstart (run locally)
- API reference
- Agent (LLM) usage
- Configuration / environment
- Development notes

---

**What it is**

- A FastAPI service exposing a `POST /scrape` endpoint that accepts a `url` and a mapping of field names to CSS selectors. The service will fetch the HTML, extract the requested fields using BeautifulSoup, save the extraction to a local SQLite DB, and return the saved id and data.
- A LangChain agent factory that exposes two tools: `fetch_webpage` and `extract_selectors`, enabling an LLM to programmatically fetch and extract pages.

**Why use it**
- Simple, clear architecture for building LLM-driven scraping flows.
- Easy to extend: add selectors normalization, custom extractor logic, or new tools for pagination, login, or headless browsing.

---

**Architecture & key components**

- `src/agent/app.py` — FastAPI application (`/scrape` endpoint). Initializes the DB on startup.
- `src/agent/agent_core.py` — LangChain agent builder exposing `fetch_webpage` and `extract_selectors` tools. Switches between OpenAI and Google Vertex AI based on config.
- `src/agent/config.py` — pydantic-based settings (reads `.env` if present).
- `src/agent/tools/http_client.py` — `fetch_webpage(url)` implemented with `httpx`.
- `src/agent/tools/html_parser.py` — BeautifulSoup CSS selector extraction (`parse_selectors`).
- `src/agent/tools/extractor.py` — wrapper around parser for normalization/validation.
- `src/agent/storage/database.py` — SQLAlchemy model + helpers to init DB and save results.
- `test_agent.py` — small local test script demonstrating extraction + DB save.

---

Quickstart (local)

Prerequisites
- Python 3.10+ (use the venv you provided)
- `requirements.txt` present in repository root

Activate your venv (use your provided command):

```powershell
& D:\Learning\ml_learning\Github\wzdm\ai_environment\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Initialize DB and run a quick test extraction (included `test_agent.py`):

```powershell
python test_agent.py
```

Start the API server (development):

```powershell
uvicorn src.agent.app:app --host 127.0.0.1 --port 8000
```

---

API Reference

POST /scrape
- Request JSON body:
  - `url` (string): URL to fetch
  - `selectors` (object): map of `fieldName` -> CSS selector (e.g. `{"title":"h1","price":".price"}`)

Example request (curl):

```bash
curl -X POST http://127.0.0.1:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","selectors":{"title":"h1"}}'
```

Example Python (requests):

```python
import requests
payload = {"url": "https://example.com", "selectors": {"title": "h1"}}
r = requests.post('http://127.0.0.1:8000/scrape', json=payload, timeout=20)
print(r.status_code, r.json())
```

Response (success):

```json
{"id": <db_id>, "status": "ok", "data": {"title": "Example Domain", ...}}
```

Errors:
- 502: fetch failed (network error or non-2xx response)
- 500: extraction failed (parser/tool error)

---

Agent / LLM Usage

The project provides `create_agent()` in `src/agent/agent_core.py`. The agent exposes two tools:
- `fetch_webpage(url: str) -> str` — returns page HTML
- `extract_selectors({"html": str, "selectors": dict}) -> dict` — returns extracted fields

Provider selection is controlled by `llm_provider` in `src/agent/config.py` (default `google`). The code supports:
- OpenAI (set `openai_api_key` environment variable or `.env`) — uses `langchain.llms.OpenAI`.
- Google Vertex AI (set `google_application_credentials`, `google_project`, `google_location`) — uses `langchain.llms.VertexAI`.

Important: running the LLM agent requires valid credentials for the chosen provider and the `langchain` package installed. The agent uses `AgentType.ZERO_SHOT_REACT_DESCRIPTION` by default.

---

Configuration / environment

Configuration lives in `src/agent/config.py` (pydantic BaseSettings). You can provide values via environment variables or a `.env` file. Key values:

- `OPENAI_API_KEY` (or `openai_api_key`) — OpenAI API key
- `GOOGLE_APPLICATION_CREDENTIALS` (or `google_application_credentials`) — path to Google service account JSON
- `GOOGLE_PROJECT` (or `google_project`)
- `GOOGLE_LOCATION` (or `google_location`) — default `us-central1`
- `LLM_PROVIDER` (or `llm_provider`) — `google` or `openai` (case-insensitive)
- `MODEL_NAME` (or `model_name`) — LLM model name (e.g. `text-bison@001` or OpenAI model)
- `DATABASE_URL` — SQLAlchemy DB URL (default `sqlite:///./agent_data.db`)
- `PORT` — app port (default `8000`)

Example `.env`:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///./agent_data.db
```

---

Database

- Default: SQLite file `agent_data.db` in the repo root (configured via `DATABASE_URL`).
- Table: `extracted_data` with `id`, `url`, `data` (text), `created_at`.
- The DB is created automatically on app startup via `init_db()` in `src/agent/storage/database.py`.

---

Development notes & extension ideas

- Add normalization/validation to `src/agent/tools/extractor.py` (currently a thin wrapper).
- Add pagination or site-specific login automation as additional tools (headless Chrome, Playwright).
- Add rate-limiting, retries, backoff, and robots.txt respect in `fetch_webpage`.
- Add authentication & authorization to the HTTP API before exposing it publicly.
- Add unit tests for parsing (`html_parser`) and integration tests for the API.

---

Docker

A `Dockerfile` is present; you can build an image and run it with environment variables for your API keys. The `uvicorn` command is used in dev; for production adapt to a proper process manager.

---

Contributing

- Open PRs for bugfixes, tests, or new features. Keep changes focused and add tests where applicable.

---

License

- No license file included by default. Add one if you intend to open-source the project.

---

If you want, I can:
- Add an example `.env` and a small `README` section showing how to run the LangChain agent demo.
- Add automated tests for the parser and API.
- Provide a `docker-compose.yml` for quick local runs.

