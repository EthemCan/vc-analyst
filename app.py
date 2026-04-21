"""Streamlit web interface for VC Analyst AI pitch deck evaluation."""

from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from main import SUPPORTED_DECK_EXTENSIONS, run_pipeline_with_text

import streamlit as st
import os

# Streamlit Cloud'da mıyız kontrol et, öyleyse keyleri oradan al
if 'OPENAI_API_KEY' in st.secrets:
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
    os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_API_KEY']
    
st.set_page_config(page_title="VC Analyst AI", page_icon=":bar_chart:", layout="centered")
st.title("VC Analyst AI: Pitch Deck Evaluator")
st.caption("Upload a startup pitch deck (.pdf or .pptx), run the analysis, and download the final PDF report.")

uploaded_file = st.file_uploader(
    "Upload pitch deck",
    type=["pdf", "pptx"],
    help="Supported formats: .pdf, .pptx",
)
report_name = st.text_input("Output PDF name", value="vc_dealflow_report.pdf")

if st.button("Start Analysis", type="primary"):
    if uploaded_file is None:
        st.error("Please upload a .pdf or .pptx file first.")
        st.stop()

    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix not in SUPPORTED_DECK_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_DECK_EXTENSIONS))
        st.error(f"Unsupported file type '{suffix}'. Supported: {supported}")
        st.stop()

    safe_report_name = report_name.strip() or "vc_dealflow_report.pdf"
    if not safe_report_name.lower().endswith(".pdf"):
        safe_report_name += ".pdf"

    with tempfile.TemporaryDirectory(prefix="vc_analyst_ai_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        input_path = tmp_path / uploaded_file.name
        output_path = tmp_path / safe_report_name

        input_path.write_bytes(uploaded_file.getbuffer())

        with st.spinner("Analyzing deck, validating market claims, and preparing your IC report..."):
            try:
                final_markdown, generated_pdf_path = run_pipeline_with_text(
                    deck_path=str(input_path),
                    output_pdf=str(output_path),
                )
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                st.stop()

        st.success("Analysis completed successfully.")
        st.subheader("Analysis Report")
        st.markdown(final_markdown)

        pdf_bytes = Path(generated_pdf_path).read_bytes()
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=safe_report_name,
            mime="application/pdf",
        )
