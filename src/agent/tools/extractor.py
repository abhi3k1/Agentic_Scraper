from .html_parser import parse_selectors


def extract_data(html: str, selectors: dict) -> dict:
    """High-level extractor that can be extended with validation/cleanup.

    Returns dict of extracted values.
    """
    data = parse_selectors(html, selectors)
    # Placeholder: add normalization/validation steps as needed
    return data
