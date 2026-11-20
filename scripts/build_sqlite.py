#!/usr/bin/env python3
"""Compile USTC-Question-Bank JSONL datasets into a single SQLite + FTS5 database."""

from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from ustc_qbank import build_sqlite  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SQLite + FTS5 database from JSONL courses.")
    parser.add_argument(
        "-o",
        "--output",
        default=str(ROOT / "dist" / "ustc-question-bank.sqlite"),
        help="Output SQLite file path (default: dist/ustc-question-bank.sqlite)",
    )
    args = parser.parse_args()
    out = build_sqlite(args.output, root=ROOT)
    size_kb = out.stat().st_size / 1024
    print(f"Built {out} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
