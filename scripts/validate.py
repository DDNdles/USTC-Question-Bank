#!/usr/bin/env python3
"""Validate USTC-Question-Bank data integrity, schema compliance, taxonomy refs,
LaTeX delimiter balance, SHA-256 checksums, and forbidden binary assets.

Zero third-party dependencies (runs cleanly on stock Python >= 3.10).
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent

ALLOWED_TYPES = {"single", "multi", "blank", "solve", "proof"}
ALLOWED_ORIGINS = {"official", "community", "ai"}
ALLOWED_SOURCE_KINDS = {"exam_paper", "book", "dataset", "notes"}
ALLOWED_EXAM_KINDS = {None, "midterm", "final", "makeup", "quiz"}
ALLOWED_RIGHTS = {
    "original",
    "third_party_exam",
    "third_party_textbook",
    "third_party_notes",
    "third_party_community",
    "third_party_textbook_and_community",
}
FORBIDDEN_SUFFIXES = {".pdf", ".sqlite", ".sqlite3", ".db", ".png", ".jpg", ".jpeg", ".zip", ".rar"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9]+-[A-Za-z0-9._-]+$")


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_latex_dollars(text: str) -> bool:
    """Return True if unescaped single/double dollar delimiters are balanced."""
    # Remove escaped \$
    cleaned = re.sub(r"\\\$", "", text)
    # Replace display $$ first
    if cleaned.count("$$") % 2 != 0:
        return False
    cleaned = cleaned.replace("$$", "")
    return cleaned.count("$") % 2 == 0


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Check forbidden binary/raw files outside .git and dist/
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if rel.parts[0] in {".git", "dist", "__pycache__"}:
            continue
        if p.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"Forbidden asset committed in repo: {rel.as_posix()}")

    # 2. Load manifest
    manifest_path = ROOT / "manifest.json"
    if not manifest_path.is_file():
        print("ERROR: manifest.json missing", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    global_ids: set[str] = set()
    total_questions = 0
    total_quarantined = 0
    total_origins: Counter = Counter()

    for c_entry in manifest["courses"]:
        code = c_entry["code"]
        c_dir = ROOT / "courses" / code
        meta_path = ROOT / c_entry["paths"]["meta"]
        tax_path = ROOT / c_entry["paths"]["taxonomy"]
        q_path = ROOT / c_entry["paths"]["questions"]

        for label, fp in (("meta", meta_path), ("taxonomy", tax_path), ("questions", q_path)):
            if not fp.is_file():
                errors.append(f"[{code}] missing file: {fp}")
                continue
            actual_hash = sha256_file(fp)
            if actual_hash != c_entry["sha256"][label]:
                errors.append(
                    f"[{code}] manifest sha256 mismatch for {label}: expected {c_entry['sha256'][label]}, got {actual_hash}"
                )

        if not (meta_path.is_file() and tax_path.is_file() and q_path.is_file()):
            continue

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        tax = json.loads(tax_path.read_text(encoding="utf-8"))

        # Check taxonomy integrity
        kp_ids: set[str] = set()
        for node in tax["nodes"]:
            nid = node["id"]
            if nid in kp_ids:
                errors.append(f"[{code}] duplicate taxonomy node: {nid}")
            kp_ids.add(nid)
        for node in tax["nodes"]:
            pid = node["parent_id"]
            if pid is not None and pid not in kp_ids:
                errors.append(f"[{code}] taxonomy node {node['id']} has missing parent {pid}")

        # Check questions.jsonl
        c_origins: Counter = Counter()
        c_quarantined = 0
        c_count = 0

        for lineno, raw_line in enumerate(q_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw_line.strip():
                errors.append(f"[{code}] blank line at questions.jsonl:{lineno}")
                continue
            try:
                q = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                errors.append(f"[{code}] invalid JSON at line {lineno}: {exc}")
                continue

            c_count += 1
            qid = q.get("id", "")
            if not ID_PATTERN.match(qid) or not qid.startswith(f"{code}-"):
                errors.append(f"[{code}:{lineno}] invalid id format: {qid!r}")
            if qid in global_ids:
                errors.append(f"[{code}:{lineno}] duplicate global id: {qid!r}")
            global_ids.add(qid)

            if q.get("course_code") != code:
                errors.append(f"[{qid}] course_code mismatch: {q.get('course_code')!r}")
            if q.get("type") not in ALLOWED_TYPES:
                errors.append(f"[{qid}] invalid type: {q.get('type')!r}")

            stem_md = (q.get("stem") or {}).get("md", "")
            ans = q.get("answer") or {}
            sol = q.get("solution") or {}
            tags = q.get("tags") or {}
            src = q.get("source") or {}
            qual = q.get("quality") or {}

            if not stem_md.strip():
                errors.append(f"[{qid}] empty stem.md")
            if not (ans.get("md") or "").strip():
                errors.append(f"[{qid}] empty answer.md")
            if ans.get("origin") not in ALLOWED_ORIGINS:
                errors.append(f"[{qid}] invalid answer.origin: {ans.get('origin')!r}")
            if not (sol.get("md") or "").strip():
                errors.append(f"[{qid}] empty solution.md")

            q_kps = tags.get("kp_ids") or []
            if not q_kps:
                errors.append(f"[{qid}] empty tags.kp_ids")
            for k in q_kps:
                if k not in kp_ids:
                    errors.append(f"[{qid}] unknown kp_id {k!r} not in taxonomy.json")

            diff = tags.get("difficulty")
            if not isinstance(diff, int) or not (1 <= diff <= 5):
                errors.append(f"[{qid}] invalid difficulty: {diff!r}")

            if src.get("kind") not in ALLOWED_SOURCE_KINDS:
                errors.append(f"[{qid}] invalid source.kind: {src.get('kind')!r}")
            if src.get("exam_kind") not in ALLOWED_EXAM_KINDS:
                errors.append(f"[{qid}] invalid source.exam_kind: {src.get('exam_kind')!r}")
            if src.get("rights") not in ALLOWED_RIGHTS:
                errors.append(f"[{qid}] invalid source.rights: {src.get('rights')!r}")

            for field_name, content in (("stem", stem_md), ("answer", ans.get("md", "")), ("solution", sol.get("md", ""))):
                if "\x00" in content:
                    errors.append(f"[{qid}] NUL byte in {field_name}")
                if not check_latex_dollars(content):
                    warnings.append(f"[{qid}] unbalanced LaTeX '$' in {field_name}")

            c_origins[ans.get("origin")] += 1
            if qual.get("quarantined"):
                c_quarantined += 1

        if c_count != meta["stats"]["total"] or c_count != c_entry["total"]:
            errors.append(
                f"[{code}] count mismatch: jsonl={c_count}, meta={meta['stats']['total']}, manifest={c_entry['total']}"
            )
        if c_quarantined != meta["stats"]["quarantined"]:
            errors.append(
                f"[{code}] quarantined count mismatch: actual={c_quarantined}, meta={meta['stats']['quarantined']}"
            )
        for origin_key in ("official", "community", "ai"):
            if c_origins[origin_key] != meta["stats"]["by_origin"][origin_key]:
                errors.append(f"[{code}] origin count mismatch for {origin_key}")

        total_questions += c_count
        total_quarantined += c_quarantined
        total_origins.update(c_origins)

    if total_questions != manifest["stats"]["questions"]:
        errors.append(
            f"manifest total questions mismatch: actual={total_questions}, manifest={manifest['stats']['questions']}"
        )
    if total_quarantined != manifest["stats"]["quarantined"]:
        errors.append(
            f"manifest quarantined mismatch: actual={total_quarantined}, manifest={manifest['stats']['quarantined']}"
        )

    print(
        f"Validated {len(manifest['courses'])} courses, {total_questions} questions "
        f"(official={total_origins['official']}, community={total_origins['community']}, "
        f"ai={total_origins['ai']}, quarantined={total_quarantined})."
    )
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings[:20]:
            print(f"  WARN: {w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more warnings")
    if errors:
        print(f"FAILED with {len(errors)} error(s):", file=sys.stderr)
        for e in errors[:30]:
            print(f"  ERROR: {e}", file=sys.stderr)
        return 1

    print("ALL CHECKS PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
