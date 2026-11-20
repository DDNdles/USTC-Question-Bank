"""Build a portable SQLite + FTS5 database from USTC-Question-Bank JSONL files."""

from __future__ import annotations

import json
import pathlib
import sqlite3

from .loader import QuestionBank

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE courses (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    name_en TEXT NOT NULL,
    department TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    total_questions INTEGER NOT NULL,
    meta_json TEXT NOT NULL
);

CREATE TABLE taxonomy (
    course_code TEXT NOT NULL REFERENCES courses(code),
    kp_id TEXT NOT NULL,
    parent_id TEXT,
    level INTEGER NOT NULL,
    name TEXT NOT NULL,
    chapter_ref TEXT,
    PRIMARY KEY (course_code, kp_id)
);

CREATE TABLE questions (
    id TEXT PRIMARY KEY,
    course_code TEXT NOT NULL REFERENCES courses(code),
    type TEXT NOT NULL,
    stem_md TEXT NOT NULL,
    answer_md TEXT NOT NULL,
    answer_origin TEXT NOT NULL,
    answer_origin_detail TEXT NOT NULL,
    solution_md TEXT NOT NULL,
    difficulty INTEGER NOT NULL,
    source_kind TEXT NOT NULL,
    source_batch TEXT NOT NULL,
    source_ref TEXT NOT NULL,
    source_year INTEGER,
    source_term TEXT,
    source_exam_kind TEXT,
    source_url TEXT,
    source_rights TEXT NOT NULL,
    quarantined INTEGER NOT NULL,
    quarantine_reason TEXT,
    confidence REAL,
    note TEXT,
    overlap_hint TEXT,
    raw_json TEXT NOT NULL
);

CREATE TABLE question_kp (
    question_id TEXT NOT NULL REFERENCES questions(id),
    course_code TEXT NOT NULL,
    kp_id TEXT NOT NULL,
    PRIMARY KEY (question_id, kp_id)
);

CREATE INDEX idx_questions_course ON questions(course_code);
CREATE INDEX idx_questions_origin ON questions(answer_origin);
CREATE INDEX idx_questions_batch ON questions(course_code, source_batch);
CREATE INDEX idx_questions_year ON questions(course_code, source_year);
CREATE INDEX idx_questions_diff ON questions(course_code, difficulty);
CREATE INDEX idx_qkp_kp ON question_kp(course_code, kp_id);

CREATE VIRTUAL TABLE questions_fts USING fts5(
    id UNINDEXED,
    course_code UNINDEXED,
    stem_md,
    answer_md,
    solution_md,
    source_ref,
    keywords,
    tokenize='unicode61'
);
"""


def build_sqlite(
    output_path: str | pathlib.Path,
    *,
    root: str | pathlib.Path | None = None,
) -> pathlib.Path:
    """Compile all courses in USTC-Question-Bank into a fresh SQLite database."""
    bank = QuestionBank(root=root)
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()

    conn = sqlite3.connect(out)
    try:
        conn.executescript(SCHEMA_SQL)
        for code in bank.course_codes:
            c = bank.course(code)
            conn.execute(
                """
                INSERT INTO courses (code, name, name_en, department, category, description, total_questions, meta_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    c.code,
                    c.meta["name"],
                    c.meta["name_en"],
                    c.meta["department"],
                    c.meta["category"],
                    c.meta["description"],
                    c.meta["stats"]["total"],
                    json.dumps(c.meta, ensure_ascii=False),
                ),
            )
            conn.executemany(
                """
                INSERT INTO taxonomy (course_code, kp_id, parent_id, level, name, chapter_ref)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (c.code, n.id, n.parent_id, n.level, n.name, n.chapter_ref)
                    for n in c.taxonomy
                ],
            )
            for q in c.questions():
                conn.execute(
                    """
                    INSERT INTO questions (
                        id, course_code, type, stem_md, answer_md,
                        answer_origin, answer_origin_detail, solution_md,
                        difficulty, source_kind, source_batch, source_ref,
                        source_year, source_term, source_exam_kind, source_url,
                        source_rights, quarantined, quarantine_reason,
                        confidence, note, overlap_hint, raw_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        q.id,
                        q.course_code,
                        q.type,
                        q.stem_md,
                        q.answer_md,
                        q.answer_origin,
                        q.answer_origin_detail,
                        q.solution_md,
                        q.difficulty,
                        q.source_kind,
                        q.source_batch,
                        q.source_ref,
                        q.source_year,
                        q.source_term,
                        q.source_exam_kind,
                        q.source_url,
                        q.source_rights,
                        1 if q.quarantined else 0,
                        q.quarantine_reason,
                        q.confidence,
                        q.note,
                        q.overlap_hint,
                        json.dumps(q.raw, ensure_ascii=False),
                    ),
                )
                conn.executemany(
                    "INSERT INTO question_kp (question_id, course_code, kp_id) VALUES (?, ?, ?)",
                    [(q.id, q.course_code, kp) for kp in q.kp_ids],
                )
                conn.execute(
                    """
                    INSERT INTO questions_fts (id, course_code, stem_md, answer_md, solution_md, source_ref, keywords)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        q.id,
                        q.course_code,
                        q.stem_md,
                        q.answer_md,
                        q.solution_md,
                        q.source_ref,
                        " ".join(q.keywords),
                    ),
                )
        conn.commit()
    finally:
        conn.close()
    return out
