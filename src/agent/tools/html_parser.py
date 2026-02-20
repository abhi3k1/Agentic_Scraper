from bs4 import BeautifulSoup
from typing import Dict, Optional


def parse_selectors(html: str, selectors: Dict[str, str]) -> Dict[str, Optional[str]]:
    """Return a dict mapping field -> extracted text or None.

    selectors: {'title': 'h1', 'price': '.price'}
    """
    soup = BeautifulSoup(html, "html.parser")
    out: Dict[str, Optional[str]] = {}
    for key, sel in selectors.items():
        el = soup.select_one(sel)
        out[key] = el.get_text(strip=True) if el else None
    return out
