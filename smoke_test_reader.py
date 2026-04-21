"""Quick smoke test for DeckReader with .pptx and .pdf inputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from deck_reader import DeckReader


def run_one(reader: DeckReader, file_path: str) -> None:
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        print(f"[FAIL] Missing file: {path}")
        return

    try:
        text = reader.extract_text(str(path))
    except Exception as exc:
        print(f"[FAIL] {path.name}: {exc}")
        return

    lines = [line for line in text.splitlines() if line.strip()]
    print(f"[OK] {path.name}: extracted {len(lines)} non-empty lines")
    preview = "\n".join(lines[:6])
    if preview:
        print("----- preview -----")
        print(preview)
        print("-------------------")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smoke test DeckReader extraction for .pptx and .pdf files."
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="One or more pitch deck paths (.pptx or .pdf) to test",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    reader = DeckReader()

    supported = {".pptx", ".pdf"}
    has_error = False
    for file_path in args.files:
        suffix = Path(file_path).suffix.lower()
        if suffix not in supported:
            print(f"[FAIL] Unsupported extension '{suffix}' for {file_path}")
            has_error = True
            continue
        run_one(reader, file_path)

    if has_error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
