"""PDF report generation for VC analysis output."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Iterable

from fpdf import FPDF


class ReportPDFGenerator:
    """Converts structured markdown-like analysis text into a professional PDF."""

    def __init__(self, title: str = "VC Deal Flow Analysis Report") -> None:
        self.title = title

    def generate(self, analysis_text: str, output_path: str) -> Path:
        """
        Create a formatted PDF from final analysis text.

        Args:
            analysis_text: Final synthesized markdown text from CrewAI.
            output_path: Desired PDF output path.

        Returns:
            Absolute path to generated PDF.

        Raises:
            ValueError: If analysis text is empty.
            RuntimeError: If PDF cannot be written.
        """
        if not analysis_text or not analysis_text.strip():
            raise ValueError("Cannot generate PDF from empty analysis text.")

        target = Path(output_path).expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)

        pdf = FPDF()
        pdf.set_margins(10, 10, 10)
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        self._write_title(pdf)
        self._write_body(pdf, analysis_text.splitlines())

        try:
            pdf.output(str(target))
        except Exception as exc:  # pragma: no cover - depends on filesystem state
            raise RuntimeError(f"Failed to write PDF at '{target}': {exc}") from exc

        return target

    def _write_title(self, pdf: FPDF) -> None:
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_x(pdf.l_margin)
        pdf.cell(0, 10, self._sanitize_pdf_text(self.title), ln=True)
        pdf.ln(3)

    def _write_body(self, pdf: FPDF, lines: Iterable[str]) -> None:
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                pdf.ln(2)
                continue

            if line.startswith("## "):
                pdf.set_font("Helvetica", "B", 13)
                header_text = line.replace("## ", "", 1)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(w=0, h=8, text=self._sanitize_pdf_text(header_text))
                pdf.ln(1)
                continue

            if line.startswith(("- ", "* ")):
                pdf.set_font("Helvetica", size=11)
                bullet_text = f"  - {line[2:].strip()}"
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(w=0, h=6, text=self._sanitize_pdf_text(bullet_text))
                continue

            if re.match(r"^\d+\.\s+", line):
                pdf.set_font("Helvetica", size=11)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(w=0, h=6, text=self._sanitize_pdf_text(line))
                continue

            pdf.set_font("Helvetica", size=11)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(w=0, h=6, text=self._sanitize_pdf_text(line))

    def _sanitize_pdf_text(self, text: str) -> str:
        """
        Normalize text to be safe for built-in Helvetica (Latin-1) fonts.

        Replaces smart punctuation with ASCII equivalents and converts any
        unsupported characters (including emojis) into '?' via latin-1 fallback.
        """
        if not text:
            return ""

        smart_replacements = {
            "\u2018": "'",  # left single quote
            "\u2019": "'",  # right single quote
            "\u201c": '"',  # left double quote
            "\u201d": '"',  # right double quote
            "\u2013": "-",  # en dash
            "\u2014": "-",  # em dash
            "\u2026": "...",  # ellipsis
            "\u00a0": " ",  # non-breaking space
        }

        normalized = text.translate(str.maketrans(smart_replacements))
        # Final safety net for characters unsupported by Latin-1 fonts.
        return normalized.encode("latin-1", "replace").decode("latin-1")
