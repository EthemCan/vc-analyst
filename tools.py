"""Tooling helpers used by CrewAI agents."""

from __future__ import annotations

import os
from typing import Any, Dict, List

from crewai.tools import BaseTool
from pydantic import PrivateAttr
from tavily import TavilyClient


class TavilyWebSearchTool(BaseTool):
    """CrewAI-compatible Tavily search tool for live web research."""

    name: str = "tavily_web_search"
    description: str = (
        "Search the live web for up-to-date market data, competitors, founders, "
        "and industry context. Input should be a concise search query."
    )
    max_results: int = 5
    _client: TavilyClient = PrivateAttr()

    def __init__(self, max_results: int = 5) -> None:
        super().__init__(max_results=max_results)
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "Missing TAVILY_API_KEY. Add it to your environment or .env file."
            )
        self._client = TavilyClient(api_key=api_key)

    def _run(self, query: str) -> str:
        """Execute Tavily search and return compact, model-friendly text."""
        try:
            response: Dict[str, Any] = self._client.search(
                # Tavily client is stored as a private attribute because BaseTool
                # uses pydantic models that disallow undeclared dynamic fields.
                # This keeps runtime clients out of serialized tool schema.
                query=query,
                search_depth="advanced",
                max_results=self.max_results,
                include_answer=True,
                include_raw_content=False,
            )
        except Exception as exc:
            return f"Tavily search failed for query '{query}': {exc}"

        answer = (response.get("answer") or "").strip()
        results: List[Dict[str, Any]] = response.get("results") or []

        lines: List[str] = []
        if answer:
            lines.append(f"Answer: {answer}")

        for idx, item in enumerate(results, start=1):
            title = (item.get("title") or "").strip()
            url = (item.get("url") or "").strip()
            snippet = (item.get("content") or "").strip()
            lines.append(
                f"{idx}. {title or 'Untitled'}\nURL: {url or 'N/A'}\nSnippet: {snippet or 'N/A'}"
            )

        return "\n\n".join(lines) if lines else "No results found."


def get_search_tool(max_results: int = 5) -> TavilyWebSearchTool:
    """
    Build a CrewAI-native live web search tool.

    Args:
        max_results: Number of top results returned by Tavily.

    Returns:
        Configured TavilyWebSearchTool instance.

    Raises:
        EnvironmentError: If TAVILY_API_KEY is missing.
    """
    return TavilyWebSearchTool(max_results=max_results)
