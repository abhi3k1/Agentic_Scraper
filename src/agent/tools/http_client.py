import httpx


def fetch_webpage(url: str, timeout: int = 15) -> str:
    """Fetch a webpage and return text content (HTML).

    Keeps a small, deterministic interface usable by the agent tools.
    """
    headers = {"User-Agent": "Agentic-Scraper/1.0 (+https://example.com)"}
    with httpx.Client(timeout=timeout, headers=headers, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.text
