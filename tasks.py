"""Task factory for the VC Deal Flow Analyzer workflow."""

from __future__ import annotations

from crewai import Task


def create_tasks(market_agent, contrarian_agent, synth_agent) -> list[Task]:
    """
    Build sequential tasks for the three-agent analysis pipeline.

    Args:
        market_agent: Market & Competitor Analyst agent.
        contrarian_agent: Contrarian VC Partner agent.
        synth_agent: Investment Committee Synthesizer agent.

    Returns:
        Ordered list of CrewAI tasks.
    """
    market_task = Task(
        description=(
            "You are given the startup pitch deck text below.\n\n"
            "{deck_text}\n\n"
            "Use live web research to validate market claims. Focus on:\n"
            "1) True market size and growth rates (with recent references)\n"
            "2) Direct competitors and hidden alternatives\n"
            "3) Any discrepancy between deck claims and public facts\n"
            "4) Founder public footprint signals (roles, reputation, track record)\n\n"
            "Cite concrete figures where possible and call out uncertainty clearly."
        ),
        expected_output=(
            "A concise market diligence memo including validated numbers, competitor "
            "map, and claim-verification notes."
        ),
        agent=market_agent,
    )

    contrarian_task = Task(
        description=(
            "SYSTEM ROLE & OBJECTIVE:\n"
            "You are a Tier-1 Silicon Valley Venture Capital Partner and Lead Analyst "
            "for an elite Angel Syndicate. You have evaluated over 5,000 early-stage "
            "(Pre-Seed/Seed) startups. Your mindset is brutally honest, deeply "
            "analytical, and highly skeptical. Your goal is to identify the 1% "
            "power-law outliers that can return 100x.\n\n"
            "TASK:\n"
            "I will provide extracted startup pitch deck text and context. Dissect "
            "the business, bypass marketing fluff, and deliver investor-ready deal "
            "flow analysis. Since this is pre-seed, assume financials are mostly "
            "directional; prioritize Founder-Market Fit, urgency of problem, early "
            "traction, and GTM viability.\n\n"
            "INPUT DECK TEXT:\n"
            "{deck_text}\n\n"
            "ANALYTICAL FRAMEWORK & REQUIRED OUTPUT:\n"
            "Output STRICT markdown with EXACTLY the sections and subsection bullets below.\n\n"
            "## 1. Executive Synthesis (The \"1-Minute Read\")\n"
            "- **The Core Thesis:** What does this company do in one sentence as if "
            "explaining to a 5-year-old.\n"
            "- **The Investment Verdict:** Definitive [STRONG YES / WEAK YES / PASS] "
            "with exactly 3 sentences of justification.\n"
            "- **The \"Why Now?\":** Why this moment in history enables this startup "
            "(technological, cultural, or regulatory shifts).\n\n"
            "## 2. Founder & Team Assessment (The Most Critical Pre-Seed Metric)\n"
            "- **Founder-Market Fit:** Why this team is uniquely qualified; identify "
            "proprietary advantage or deep domain expertise.\n"
            "- **Execution Capability:** Evidence of builders (shipping fast) versus "
            "talkers.\n"
            "- **Missing Roles:** Key missing talent required over next 18 months.\n\n"
            "## 3. Problem & Market Urgency\n"
            "- **Vitamin vs. Painkiller:** Is this mission-critical pain or nice-to-have?\n"
            "- **TAM/SAM/SOM Reality Check:** Ignore inflated top-down figures and "
            "estimate realistic SOM capturable in 24 months.\n"
            "- **Incumbent Vulnerability:** Current dinosaurs and why they may fail to "
            "crush this startup.\n\n"
            "## 4. Product, Solution & Defensibility (The Moat)\n"
            "- **The \"Unfair Advantage\":** True moat (data network effects, deep "
            "tech, community lock-in, etc.).\n"
            "- **Friction Points:** Biggest adoption barrier and key objection reason.\n"
            "- **Invisible Competitors:** Exactly 3 alternative current behaviors "
            "(e.g., spreadsheets, manual ops, ignoring problem).\n\n"
            "## 5. Go-To-Market (GTM) & Traction (Signs of Life)\n"
            "- **The First 100 True Fans:** Evaluate realism of first 100/1,000 paying "
            "user acquisition strategy.\n"
            "- **Early Signals:** Authentic traction evidence (waitlists, LOIs, beta "
            "usage, engagement).\n"
            "- **Unit Economics Viability:** Estimate CAC vs LTV reality and whether "
            "distribution model fits price point.\n\n"
            "## 6. Risk Mitigation & Financial Survival\n"
            "- **Burn Rate & Runway:** Infer runway from requested funding and flag if "
            "under 18 months.\n"
            "- **The \"Fatal Flaw\":** Single most likely reason the startup dies in "
            "12 months, with specificity.\n"
            "- **Seed Round Milestones:** Precise milestones required to raise next round.\n\n"
            "## 7. The Interrogation Room (Meeting Prep)\n"
            "Provide exactly 3 aggressive probing questions to test founder resilience, "
            "strategic depth, and core assumptions.\n\n"
            "FORMATTING RULES:\n"
            "- Use professional VC terminology (CAC, LTV, Burn Rate, Churn, PMF, "
            "Network Effects).\n"
            "- Be concise. Use bullet points and bold text for emphasis.\n"
            "- Do not hallucinate data. If information is missing, explicitly state: "
            "\"WARNING: No data provided regarding [Topic].\""
        ),
        expected_output=(
            "Strict markdown that includes sections 1 through 7 exactly as specified, "
            "uses concise bullet points with bold labels, contains exactly one verdict "
            "of [STRONG YES/WEAK YES/PASS], and includes explicit WARNING statements "
            "for any missing data."
        ),
        agent=contrarian_agent,
    )

    synthesis_task = Task(
        description=(
            "Synthesize the Market & Competitor Analyst output with the full "
            "Contrarian VC Partner 7-step analysis into one final executive report "
            "for PDF generation.\n\n"
            "CRITICAL OBJECTIVE:\n"
            "- Preserve analytical depth from the full 7-step contrarian framework.\n"
            "- Do NOT compress into a short memo that loses nuance.\n"
            "- Keep all high-signal risk, GTM, moat, and interrogation insights.\n\n"
            "OUTPUT FORMAT (STRICT MARKDOWN):\n"
            "Use EXACTLY these section headers and keep subsection bullet labels "
            "explicitly visible for PDF readability:\n\n"
            "## 1. Executive Synthesis (The \"1-Minute Read\")\n"
            "- **The Core Thesis:**\n"
            "- **The Investment Verdict:**\n"
            "- **The \"Why Now?\":**\n\n"
            "## 2. Founder & Team Assessment (The Most Critical Pre-Seed Metric)\n"
            "- **Founder-Market Fit:**\n"
            "- **Execution Capability:**\n"
            "- **Missing Roles:**\n\n"
            "## 3. Problem & Market Urgency\n"
            "- **Vitamin vs. Painkiller:**\n"
            "- **TAM/SAM/SOM Reality Check:**\n"
            "- **Incumbent Vulnerability:**\n\n"
            "## 4. Product, Solution & Defensibility (The Moat)\n"
            "- **The \"Unfair Advantage\":**\n"
            "- **Friction Points:**\n"
            "- **Invisible Competitors:**\n\n"
            "## 5. Go-To-Market (GTM) & Traction (Signs of Life)\n"
            "- **The First 100 True Fans:**\n"
            "- **Early Signals:**\n"
            "- **Unit Economics Viability:**\n\n"
            "## 6. Risk Mitigation & Financial Survival\n"
            "- **Burn Rate & Runway:**\n"
            "- **The \"Fatal Flaw\":**\n"
            "- **Seed Round Milestones:**\n\n"
            "## 7. The Interrogation Room (Meeting Prep)\n"
            "1. \n"
            "2. \n"
            "3. \n\n"
            "INTEGRATION RULES:\n"
            "- Resolve conflicts between sources by preferring externally validated "
            "market evidence from the market analyst, while retaining contrarian "
            "reasoning depth.\n"
            "- Preserve exactly one definitive verdict: [STRONG YES / WEAK YES / PASS].\n"
            "- Preserve all critical findings; do not omit fatal risks.\n"
            "- Keep exactly 3 numbered interrogation questions.\n"
            "- Use VC terminology (CAC, LTV, Burn Rate, Churn, PMF, Network Effects).\n"
            "- If data is missing for any required area, state exactly: "
            "\"WARNING: No data provided regarding [Topic].\"\n"
            "- Do not include preface, appendix, or additional sections."
        ),
        expected_output=(
            "Strict markdown executive report with all 7 sections and required "
            "subsection bullets, one definitive verdict, exactly 3 numbered "
            "interrogation questions, and explicit WARNING lines for missing data."
        ),
        agent=synth_agent,
        context=[market_task, contrarian_task],
    )

    return [market_task, contrarian_task, synthesis_task]
