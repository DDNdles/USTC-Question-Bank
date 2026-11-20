"""Unit tests for ustc_qbank loader and SQLite FTS5 builder."""

from __future__ import annotations

import pathlib
import sqlite3
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from ustc_qbank import QuestionBank, build_sqlite  # noqa: E402


class TestQuestionBank(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = QuestionBank(ROOT)

    def test_courses_and_totals(self) -> None:
        self.assertEqual(self.bank.course_codes, ["001548", "MATH1006", "MATH1007"])
        self.assertEqual(len(self.bank["001548"]), 571)
        self.assertEqual(len(self.bank["MATH1006"]), 445)
        self.assertEqual(len(self.bank["MATH1007"]), 569)
        self.assertEqual(len(self.bank.all_questions()), 1585)
        self.assertEqual(len(self.bank.all_questions(exclude_quarantined=True)), 1578)

    def test_lookup_by_id(self) -> None:
        q = self.bank.get("MATH1006-tb-1.1.1")
        self.assertEqual(q.course_code, "MATH1006")
        self.assertEqual(q.answer_origin, "community")
        self.assertTrue(len(q.stem_md) > 0)

    def test_taxonomy_subtree_query(self) -> None:
        c = self.bank["MATH1006"]
        lim_qs = c.query(kp="ma1.lim")
        self.assertGreater(len(lim_qs), 50)
        expanded = c.expand_kp("ma1.lim")
        for q in lim_qs:
            self.assertTrue(expanded.intersection(q.kp_ids))

    def test_filters_and_sampling(self) -> None:
        c = self.bank["001548"]
        clean_exams = c.query(
            source_kinds=["exam_paper"],
            origins=["official"],
            exclude_quarantined=True,
        )
        self.assertGreater(len(clean_exams), 40)
        self.assertTrue(all(not q.quarantined for q in clean_exams))
        self.assertTrue(all(q.answer_origin == "official" for q in clean_exams))

        s1 = c.sample(10, seed=42, exclude_batches=["yan_mp_part1"])
        s2 = c.sample(10, seed=42, exclude_batches=["yan_mp_part1"])
        self.assertEqual([q.id for q in s1], [q.id for q in s2])
        self.assertTrue(all(q.source_batch != "yan_mp_part1" for q in s1))

    def test_figures_and_asset_resolution(self) -> None:
        c = self.bank["001548"]
        self.assertEqual(len(c.query(has_figures=True)), 0)
        local_resolved = c.resolve_asset("assets/demo.svg")
        self.assertTrue(local_resolved.endswith(str(pathlib.Path("courses") / "001548" / "assets" / "demo.svg")))
        c_cdn = type(c)(ROOT, "001548", asset_base_url="https://cdn.example.com/qbank")
        self.assertEqual(
            c_cdn.resolve_asset("assets/demo.svg"),
            "https://cdn.example.com/qbank/courses/001548/assets/demo.svg",
        )

    def test_build_sqlite_and_fts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = build_sqlite(pathlib.Path(tmp) / "qbank.sqlite", root=ROOT)
            conn = sqlite3.connect(db_path)
            try:
                count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
                self.assertEqual(count, 1585)
                hits = conn.execute(
                    "SELECT id FROM questions_fts WHERE questions_fts MATCH 'Laurent' LIMIT 5"
                ).fetchall()
                self.assertGreater(len(hits), 0)
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
