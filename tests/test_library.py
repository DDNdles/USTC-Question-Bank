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
        self.assertEqual(
            self.bank.course_codes,
            [
                "001548",
                "MATH1006",
                "MATH1007",
                "MATH1009",
                "CS1003",
                "PHYS1001A",
                "PHYS1002A",
                "PHYS1004A",
                "210070",
                "STAT2002",
                "PHYS1003A",
                "210050",
                "023181",
                "EE2003",
            ],
        )
        self.assertEqual(len(self.bank["001548"]), 571)
        self.assertEqual(len(self.bank["MATH1006"]), 445)
        self.assertEqual(len(self.bank["MATH1007"]), 569)
        self.assertEqual(len(self.bank["MATH1009"]), 885)
        self.assertEqual(len(self.bank["CS1003"]), 1533)
        self.assertEqual(len(self.bank["PHYS1001A"]), 253)
        self.assertEqual(len(self.bank["PHYS1002A"]), 352)
        self.assertEqual(len(self.bank["PHYS1004A"]), 121)
        self.assertEqual(len(self.bank["210070"]), 347)
        self.assertEqual(len(self.bank["STAT2002"]), 431)
        self.assertEqual(len(self.bank["PHYS1003A"]), 228)
        self.assertEqual(len(self.bank["210050"]), 512)
        self.assertEqual(len(self.bank["023181"]), 407)
        self.assertEqual(len(self.bank["EE2003"]), 505)
        self.assertEqual(len(self.bank.all_questions()), 7159)
        self.assertEqual(len(self.bank.all_questions(exclude_quarantined=True)), 7124)

    def test_lookup_by_id(self) -> None:
        q = self.bank.get("MATH1006-tb-1.1.1")
        self.assertEqual(q.course_code, "MATH1006")
        self.assertEqual(q.answer_origin, "community")
        self.assertTrue(len(q.stem_md) > 0)

        q_la = self.bank.get("MATH1009-tb-1.1.1")
        self.assertEqual(q_la.course_code, "MATH1009")
        self.assertEqual(q_la.answer_origin, "official")
        self.assertTrue(len(q_la.stem_md) > 0)

        q_cs = self.bank.get("CS1003-bank-2009-001")
        self.assertEqual(q_cs.course_code, "CS1003")
        self.assertEqual(q_cs.type, "single")
        self.assertGreaterEqual(len(q_cs.options), 4)

        q_phys = self.bank.get("PHYS1001A-exam-2025f-f-03")
        self.assertEqual(q_phys.course_code, "PHYS1001A")
        self.assertEqual(q_phys.answer_origin, "official")
        self.assertEqual(len(q_phys.stem_figures), 1)

        q_therm = self.bank.get("PHYS1002A-exam-2017-f-03")
        self.assertEqual(q_therm.course_code, "PHYS1002A")
        self.assertEqual(q_therm.answer_origin, "official")
        self.assertEqual(len(q_therm.stem_figures), 1)

        q_em = self.bank.get("PHYS1004A-exam-2017s-f-01")
        self.assertEqual(q_em.course_code, "PHYS1004A")
        self.assertEqual(q_em.answer_origin, "official")
        self.assertEqual(len(q_em.stem_figures), 1)

        q_ds = self.bank.get("210070-exam-2008f-f-25")
        self.assertEqual(q_ds.course_code, "210070")
        self.assertEqual(q_ds.answer_origin, "community")
        self.assertEqual(len(q_ds.stem_figures), 1)

        q_stat = self.bank.get("STAT2002-exam-2003s-f-01")
        self.assertEqual(q_stat.course_code, "STAT2002")
        self.assertEqual(q_stat.answer_origin, "ai")
        self.assertEqual(len(q_stat.stem_figures), 1)

        q_opt = self.bank.get("PHYS1003A-exam-2021f-f-11")
        self.assertEqual(q_opt.course_code, "PHYS1003A")
        self.assertEqual(q_opt.answer_origin, "official")
        self.assertEqual(len(q_opt.stem_figures), 1)

        q_dl = self.bank.get("210050-exam-2015f-f-14")
        self.assertEqual(q_dl.course_code, "210050")
        self.assertEqual(q_dl.answer_origin, "official")
        self.assertEqual(len(q_dl.stem_figures), 1)

        q_dl_book = self.bank.get("210050-tb-hw-4.10")
        self.assertEqual(q_dl_book.course_code, "210050")
        self.assertEqual(q_dl_book.answer_origin, "official")
        self.assertEqual(len(q_dl_book.stem_figures), 1)
        self.assertEqual(len(q_dl_book.solution_figures), 1)

        q_le = self.bank.get("023181-tb-ex-1.3.5")
        self.assertEqual(q_le.course_code, "023181")
        self.assertEqual(q_le.answer_origin, "official")
        self.assertEqual(len(q_le.stem_figures), 1)
        self.assertEqual(len(q_le.solution_figures), 1)

        q_ce = self.bank.get("EE2003-tb-hw-4.23")
        self.assertEqual(q_ce.course_code, "EE2003")
        self.assertEqual(q_ce.answer_origin, "official")
        self.assertEqual(len(q_ce.stem_figures), 1)

        q_ce_sol = self.bank.get("EE2003-tb-hw-2.6")
        self.assertEqual(q_ce_sol.course_code, "EE2003")
        self.assertEqual(q_ce_sol.answer_origin, "official")
        self.assertEqual(len(q_ce_sol.solution_figures), 1)

        q_ce_supp = self.bank.get("EE2003-supp-4.62")
        self.assertEqual(q_ce_supp.course_code, "EE2003")
        self.assertEqual(q_ce_supp.answer_origin, "official")
        self.assertEqual(len(q_ce_supp.stem_figures), 1)

    def test_taxonomy_subtree_query(self) -> None:
        c = self.bank["MATH1006"]
        lim_qs = c.query(kp="ma1.lim")
        self.assertGreater(len(lim_qs), 50)
        expanded = c.expand_kp("ma1.lim")
        for q in lim_qs:
            self.assertTrue(expanded.intersection(q.kp_ids))

        la_qs = self.bank["MATH1009"].query(kp="la1.map")
        self.assertGreater(len(la_qs), 100)

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

        phys = self.bank["PHYS1001A"]
        with_figs = phys.query(has_figures=True, exclude_quarantined=False)
        self.assertEqual(len(with_figs), 86)
        self.assertEqual(len(phys.query(has_figures=True)), 84)
        for q in with_figs:
            for fg in (*q.stem_figures, *q.solution_figures):
                self.assertTrue(pathlib.Path(phys.resolve_asset(fg.path)).is_file())

        for code_check, exp_all, exp_clean in [
            ("PHYS1002A", 48, 48),
            ("PHYS1004A", 58, 54),
            ("210070", 17, 17),
            ("STAT2002", 1, 1),
            ("PHYS1003A", 20, 19),
            ("210050", 362, 362),
            ("023181", 319, 319),
            ("EE2003", 20, 17),
        ]:
            cb = self.bank[code_check]
            wf = cb.query(has_figures=True, exclude_quarantined=False)
            self.assertEqual(len(wf), exp_all)
            self.assertEqual(len(cb.query(has_figures=True)), exp_clean)
            for q in wf:
                for fg in (*q.stem_figures, *q.solution_figures):
                    self.assertTrue(pathlib.Path(cb.resolve_asset(fg.path)).is_file())

    def test_build_sqlite_and_fts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = build_sqlite(pathlib.Path(tmp) / "qbank.sqlite", root=ROOT)
            conn = sqlite3.connect(db_path)
            try:
                count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
                self.assertEqual(count, 7159)
                hits = conn.execute(
                    "SELECT id FROM questions_fts WHERE questions_fts MATCH 'Laurent' LIMIT 5"
                ).fetchall()
                self.assertGreater(len(hits), 0)
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
