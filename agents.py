"""Agent factory for the VC Deal Flow Analyzer."""

from __future__ import annotations

from crewai import Agent

from tools import get_search_tool


def create_agents() -> tuple[Agent, Agent, Agent]:
    """
    Create all core agents used by the Crew.

    Returns:
        Tuple of agents in execution order:
        (market_analyst, contrarian_partner, committee_synthesizer)
    """
    search_tool = get_search_tool()

    market_analyst = Agent(
        role="Market & Competitor Analyst",
        goal=(
            "Validate market claims with live data and identify direct, indirect, "
            "and hidden competitors."
        ),
        backstory=(
            "You are a relentless market intelligence operator for top-tier VC firms. "
            "You verify TAM/SAM/SOM claims, check category growth rates, and uncover "
            "unexpected alternatives startups compete against."
        ),
        tools=[search_tool],
        verbose=True,
        allow_delegation=False,
    )

    contrarian_partner = Agent(
        role="Contrarian VC Partner",
        goal=(
            "Dissect pre-seed startups with brutal rigor to identify power-law "
            "outliers that can return 100x while exposing fatal risks."
        ),
        backstory=(
            "You are a Tier-1 Silicon Valley Venture Capital Partner and Lead "
            "Analyst for an elite Angel Syndicate. You have evaluated 5,000+ "
            "pre-seed and seed startups with a highly skeptical, evidence-first "
            "mindset. You ignore marketing fluff, prioritize Founder-Market Fit, "
            "problem urgency, early traction, GTM viability, and capital survival. "
            "Your work product is concise, investor-ready, and intellectually "
            "unforgiving."
        ),
        verbose=True,
        allow_delegation=False,
    )

    investment_committee = Agent(
        role="Investment Committee Synthesizer",
        goal=(
            "Combine market evidence and contrarian analysis into a concise, "
            "executive-level recommendation suitable for an investment committee."
        ),
        backstory=(
            "You prepare IC memos under tight deadlines. Your writing is brutally "
            "clear, evidence-based, and focused on investability risks."
        ),
        verbose=True,
        allow_delegation=False,
    )

    return market_analyst, contrarian_partner, investment_committee
