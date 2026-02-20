import os
from typing import Dict, Any
from langchain.agents import create_agent as lc_create_agent
from .tools.http_client import fetch_webpage
from .tools.extractor import extract_data
from .config import settings


def _fetch_webpage_wrapper(url: str) -> str:
    """Fetch a webpage HTML given a URL.

    Input: `url` (str)
    Returns: HTML text (str)
    """
    return fetch_webpage(url)


def _extract_wrapper(inputs: Dict[str, Any]) -> dict:
    """Extract fields from HTML using provided selectors.

    Input: dict with keys `html` (str) and `selectors` (dict).
    Returns: dict of extracted fields.
    """
    html = inputs.get("html")
    selectors = inputs.get("selectors", {})
    if not html:
        return {"error": "missing html"}
    return extract_data(html, selectors)


def create_agent():
    """Create and return a LangChain agent with the fetch and extract tools.

    The agent is initialized lazily by the app and reused.
    """
    # Pass simple callables as tools. `create_agent` will accept callables
    # and use their function names as tool identifiers.
    tools = [_fetch_webpage_wrapper, _extract_wrapper]

    # Build a model identifier string for `create_agent` so LangChain can
    # initialize the appropriate chat model via its factory. This avoids
    # importing provider-specific chat model classes that may not be
    # available across LangChain versions.
    provider = getattr(settings, "llm_provider", "").lower()
    if provider == "google_genai":
        model_id = f"google_genai:{settings.model_name}"
    else:
        model_id = f"openai:{settings.model_name}"

    agent = lc_create_agent(model=model_id, tools=tools, system_prompt="You are an automated web scraper assistant.")
    return agent
