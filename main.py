"""Entry point for the multi-agent VC Deal Flow Analyzer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from crewai import Crew, Process
from dotenv import load_dotenv

from agents import create_agents
from deck_reader import DeckReader
from pdf_generator import ReportPDFGenerator
from tasks import create_tasks

SUPPORTED_DECK_EXTENSIONS = {".pptx", ".pdf"}


def run_pipeline_with_text(deck_path: str, output_pdf: str) -> tuple[str, Path]:
    """
    Execute the full analysis pipeline and produce analysis text + PDF report.

    Args:
        deck_path: Path to input .pptx or .pdf file.
        output_pdf: Path where the output PDF should be saved.

    Returns:
        Tuple of (final markdown analysis, generated PDF path).
    """
    load_dotenv()

    # 1) Extract deck text.
    reader = DeckReader()
    deck_text = reader.extract_text(deck_path)

    # 2) Build agents and tasks.
    market_agent, contrarian_agent, synth_agent = create_agents()
    tasks = create_tasks(market_agent, contrarian_agent, synth_agent)

    # 3) Run CrewAI workflow.
    crew = Crew(
        agents=[market_agent, contrarian_agent, synth_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    try:
        result = crew.kickoff(inputs={"deck_text": deck_text})
    except Exception as exc:
        raise RuntimeError(f"Crew execution failed: {exc}") from exc

    final_text = str(result).strip()
    if not final_text:
        raise RuntimeError("Crew returned empty output. Cannot create report.")

    # 4) Generate final PDF.
    pdf_writer = ReportPDFGenerator()
    pdf_path = pdf_writer.generate(analysis_text=final_text, output_path=output_pdf)
    return final_text, pdf_path


def run_pipeline(deck_path: str, output_pdf: str) -> Path:
    """
    Backward-compatible wrapper that returns only the PDF path.

    Args:
        deck_path: Path to input .pptx or .pdf file.
        output_pdf: Path where the output PDF should be saved.

    Returns:
        Path to generated PDF.
    """
    _, pdf_path = run_pipeline_with_text(deck_path=deck_path, output_pdf=output_pdf)
    return pdf_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multi-agent VC Deal Flow Analyzer for startup pitch decks."
    )
    parser.add_argument("deck_path", help="Path to input .pptx or .pdf pitch deck")
    parser.add_argument(
        "--output",
        default="vc_dealflow_report.pdf",
        help="Output PDF path (default: vc_dealflow_report.pdf)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    deck_path = Path(args.deck_path).expanduser().resolve()

    if not deck_path.exists():
        print(f"Error: Input file does not exist -> {deck_path}", file=sys.stderr)
        raise SystemExit(1)
    if deck_path.suffix.lower() not in SUPPORTED_DECK_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_DECK_EXTENSIONS))
        print(
            f"Error: Unsupported input type '{deck_path.suffix}'. Supported: {supported}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        pdf_path = run_pipeline(str(deck_path), args.output)
    except Exception as exc:
        print(f"Pipeline failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"Success: Report generated at {pdf_path}")


if __name__ == "__main__":
    main()
