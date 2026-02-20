# Agentic Scraper (LangChain)

A small, extensible web-scraping microservice and LangChain agent that fetches pages, extracts fields via CSS selectors, and stores the results in SQLite. The repository provides a FastAPI HTTP endpoint for direct scraping requests and a LangChain agent with two tools (fetch + extract) that can be used by an LLM to orchestrate scraping tasks.
