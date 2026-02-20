import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from .tools.http_client import fetch_webpage
from .tools.extractor import extract_data
from .storage.database import init_db, save_extraction
from .config import settings


class ScrapeRequest(BaseModel):
    url: str
    selectors: Dict[str, str]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB on startup
    init_db()
    yield


app = FastAPI(title="Agentic Scraper", lifespan=lifespan)


@app.post("/scrape")
def scrape(req: ScrapeRequest):
    try:
        html = fetch_webpage(req.url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"fetch failed: {e}")

    try:
        parsed = extract_data(html, req.selectors)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"extract failed: {e}")

    db_id = save_extraction(req.url, parsed)
    return {"id": db_id, "status": "ok", "data": parsed}

