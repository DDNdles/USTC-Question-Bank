#!/usr/bin/env python3
"""Validate USTC-Question-Bank data integrity, schema compliance, taxonomy refs,
figure asset rules, LaTeX delimiter balance, SHA-256 checksums, and forbidden assets.

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
ALLOWED_ASSET_SUFFIXES = {".svg", ".webp", ".png"}
MAX_ASSET_BYTES = 500 * 1024  # 500 KB per figure
FORBIDDEN_SUFFIXES = {".pdf", ".sqlite", ".sqlite3", ".db", ".zip", ".rar", ".jpg", ".jpeg"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9]+-[A-Za-z0-9._-]+$")
ASSET_PATH_PATTERN = re.compile(r"^assets/[A-Za-z0-9._/-]+\.(svg|webp|png)$")


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_latex_dollars(text: str) -> bool:
    """Return True if unescaped single/double dollar delimiters are balanced."""
    cleaned = re.sub(r"\\\$", "", text)
    if cleaned.count("$$") % 2 != 0:
        return False
    cleaned = cleaned.replace("$$", "")
    return cleaned.count("$") % 2 == 0


def validate_figures(
    qid: str,
    course_dir: pathlib.Path,
    figures: list,
    asset_base_url: str | None,
    referenced_assets: set[str],
    errors: list[str],
) -> None:
    if not isinstance(figures, list):
        errors.append(f"[{qid}] figures must be an array")
        return
    for fig in figures:
        fpath = fig.get("path", "")
        if not ASSET_PATH_PATTERN.match(fpath):
            errors.append(f"[{qid}] invalid figure path {fpath!r} (expected assets/*.svg|webp|png)")
            continue
        if not (fig.get("alt") or "").strip():
            errors.append(f"[{qid}] figure {fpath!r} missing alt text")
        referenced_assets.add(fpath)
        if asset_base_url is None:
            local_asset = course_dir / fpath
            if not local_asset.is_file():
                errors.append(f"[{qid}] missing local figure file: {local_asset.relative_to(ROOT).as_posix()}")
            else:
                if local_asset.stat().st_size > MAX_ASSET_BYTES:
                    errors.append(
                        f"[{qid}] figure {fpath} exceeds {MAX_ASSET_BYTES // 1024} KB limit"
                    )
                expected_sha = fig.get("sha256")
                if expected_sha and sha256_file(local_asset) != expected_sha:
                    errors.append(f"[{qid}] figure sha256 mismatch for {fpath}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Check forbidden raw/binary files outside .git and dist/
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if rel.parts[0] in {".git", "dist", "__pycache__"}:
            continue
        suf = p.suffix.lower()
        if suf in FORBIDDEN_SUFFIXES:
            errors.append(f"Forbidden asset committed in repo: {rel.as_posix()}")
        elif suf in ALLOWED_ASSET_SUFFIXES:
            # Image assets are only allowed inside courses/<course_code>/assets/
            if not (len(rel.parts) >= 4 and rel.parts[0] == "courses" and rel.parts[2] == "assets"):
                errors.append(
                    f"Image asset outside courses/<code >/assets/: {rel.as_posix()}"
                )
            elif p.stat().st_size > MAX_ASSET_BYTES:
                errors.append(
                    f"Image asset exceeds {MAX_ASSET_BYTES // 1024} KB limit: {rel.as_posix()}"
                )

    # 2. Load manifest
    manifest_path = ROOT / "manifest.json"
    if not manifest_path.is_file():
        print("ERROR: manifest.json missing", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    asset_base_url: str | None = manifest.get("asset_base_url")

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

        c_origins: Counter = Counter()
        c_quarantined = 0
        c_count = 0
        referenced_assets: set[str] = set()

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
            qtype = q.get("type")
            if qtype not in ALLOWED_TYPES:
                errors.append(f"[{qid}] invalid type: {qtype!r}")

            stem = q.get("stem") or {}
            stem_md = stem.get("md", "")
            options = q.get("options")
            ans = q.get("answer") or {}
            sol = q.get("solution") or {}
            tags = q.get("tags") or {}
            src = q.get("source") or {}
            qual = q.get("quality") or {}

            if not stem_md.strip():
                errors.append(f"[{qid}] empty stem.md")
            if not isinstance(options, list):
                errors.append(f"[{qid}] options must be an array")
            elif qtype in {"single", "multi"} and len(options) < 2:
                errors.append(f"[{qid}] choice question ({qtype}) requires at least 2 options")

            validate_figures(qid, c_dir, stem.get("figures", []), asset_base_url, referenced_assets, errors)
            validate_figures(qid, c_dir, ans.get("figures", []), asset_base_url, referenced_assets, errors)
            validate_figures(qid, c_dir, sol.get("figures", []), asset_base_url, referenced_assets, errors)
            if isinstance(options, list):
                for opt in options:
                    validate_figures(
                        qid, c_dir, opt.get("figures", []), asset_base_url, referenced_assets, errors
                    )

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

        # Ensure no unreferenced orphan images under courses/<code>/assets/
        assets_dir = c_dir / "assets"
        if assets_dir.is_dir():
            for asset in assets_dir.rglob("*"):
                if asset.is_file():
                    rel_asset = asset.relative_to(c_dir).as_posix()
                    if rel_asset not in referenced_assets:
                        errors.append(f"[{code}] unreferenced orphan asset: {rel_asset}")

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
