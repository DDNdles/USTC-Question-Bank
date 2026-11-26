"""Regression tests guarding data quality invariants and GitHub Issue #1 fixes."""

from __future__ import annotations

import pathlib
import re
import unittest

from ustc_qbank import QuestionBank  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


class TestQualityRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = QuestionBank(ROOT)

    def test_version_and_no_control_chars(self) -> None:
        self.assertEqual(self.bank.manifest["data_version"], "0.21.0")
        for q in self.bank.all_questions():
            texts = [q.stem_md, q.answer_md, q.solution_md, q.note or "", *q.solution_steps]
            texts.extend(opt.md for opt in q.options)
            for txt in texts:
                self.assertIsNone(CTRL_RE.search(txt), f"Control char found in {q.id}: {txt!r}")

    def test_choice_answer_option_consistency(self) -> None:
        for q in self.bank.all_questions():
            opt_keys = {opt.key for opt in q.options}
            ans = q.answer_md.strip()
            if q.type == "single":
                self.assertGreaterEqual(len(opt_keys), 2, f"{q.id} missing options")
                self.assertIn(ans, opt_keys, f"{q.id} single answer {ans!r} not in {sorted(opt_keys)}")
            elif q.type == "multi":
                self.assertGreaterEqual(len(opt_keys), 2, f"{q.id} missing options")
                letters = set(re.findall(r"[A-G]", ans))
                self.assertGreaterEqual(len(letters), 2, f"{q.id} multi answer {ans!r} has <2 keys")
                self.assertTrue(letters.issubset(opt_keys), f"{q.id} multi keys {letters} not subset of {opt_keys}")

    def test_marx_issue1_and_no_spun_bleed(self) -> None:
        self.assertEqual(self.bank.get("MARX1011-misc3-034").answer_md, "错误")
        self.assertEqual(self.bank.get("MARX1011-kaoyan-judge-023").answer_md, "错误")
        self.assertEqual(self.bank.get("MARX1011-kaoyan-bank-003").answer_md, "错误")
        self.assertIn("（3）科学文化实践", self.bank.get("MARX1011-rev2018-009").solution_md)
        self.assertNotIn(
            "第一，实践是改造世界的客观物质活动，具有直接现实性。\n第一，",
            self.bank.get("MARX1011-rev2018-009").answer_md,
        )
        self.assertNotIn("近年来资本主义社会发生了哪些新变化", self.bank.get("MARX1011-tb2023-016").solution_md)
        self.assertIn("辩证否定观", self.bank.get("MARX1011-judge-v1-009").solution_md)
        self.assertIn("革命性", self.bank.get("MARX1011-kaoyan-bank-008").solution_md)
        for q in self.bank["MARX1011"]:
            self.assertNotIn("必须坚持的原则是什么", q.stem_md, f"Spun stem in {q.id}")
            self.assertNotIn("的道理去解析", q.stem_md, f"Spun stem in {q.id}")
            self.assertNotIn("的详细做法", q.stem_md, f"Spun stem in {q.id}")

    def test_cs_ds_dm_stat_phys_issue1_fixes(self) -> None:
        # 210070
        self.assertEqual(self.bank.get("210070-exam-2018f-f-09").answer_md, "C")
        self.assertEqual(self.bank.get("210070-exam-2018f-f-27").answer_md, "81")
        self.assertEqual(self.bank.get("210070-exam-2008f-f-23").answer_md, "地址依次为：100, 1084, 1256")
        self.assertIn(r"\left(\frac{1}{2}+n\right)i", self.bank.get("210070-drill-chap1024-22").solution_md)
        self.assertNotIn("92>65", self.bank.get("210070-drill-chap3579-02").solution_md)
        self.assertEqual(self.bank.get("210070-drill-chap1024-07").answer_md, "×")
        q_scc = self.bank.get("210070-drill-chap3579-16")
        self.assertIn("v6→3→2", q_scc.solution_md)
        self.assertNotIn("v5 只有入边", q_scc.solution_md)
        q_bst = self.bank.get("210070-drill-chap2468-24")
        self.assertIn("bool IsSearchTree(Bitree T, Elemtype &e)", q_bst.answer_md)
        self.assertIn("<=", q_bst.answer_md)

        # 229001
        self.assertIn("(13)(24)(5)", self.bank.get("229001-sol-c8-01").answer_md)
        self.assertEqual(self.bank.get("229001-sol-c8-07").answer_md, "$108$")
        self.assertEqual(self.bank.get("229001-sol-c8-06").answer_md, "$38$")
        self.assertIn("范数绝对值为 $2$", self.bank.get("229001-hw2-14").solution_md)
        q_combi13 = self.bank.get("229001-sol-combi-13")
        self.assertIn("6$ 个入口", q_combi13.stem_md)
        self.assertEqual(len(q_combi13.stem_figures), 1)
        self.assertTrue(pathlib.Path(self.bank["229001"].resolve_asset(q_combi13.stem_figures[0].path)).is_file())

        # STAT2002
        self.assertEqual(self.bank.get("STAT2002-exam-2020s-f-09").answer_md, "D")
        self.assertIn("N(-0.36,1)", self.bank.get("STAT2002-exam-2024s-f-14").solution_md)
        self.assertNotIn("N(-1.8,1)", self.bank.get("STAT2002-exam-2024s-f-14").solution_md)

        # CS1002A & CS1003 & PHYS1005A
        q_csa17 = self.bank.get("CS1002A-exam-2023f-m-17")
        self.assertEqual(len(q_csa17.stem_figures), 3)
        self.assertIn("只有 **c**", self.bank.get("CS1002A-hw4-04").answer_md)
        self.assertEqual(self.bank.get("CS1003-exam-2025f-f-24").answer_md, "DE")
        self.assertEqual(self.bank.get("PHYS1005A-exam-2026-f-01").answer_md, "B")
        self.assertEqual(self.bank.get("PHYS1005A-exam-2026-f-03").answer_md, "B")

    def test_new12_courses_quality_invariants(self) -> None:
        new_codes = [
            "022392", "022057", "001506", "001505", "MATH3008", "MATH3002",
            "MATH3007", "MATH3001", "017063", "017129", "001101", "001122",
            "MATH2004", "011103", "210045", "MATH2003",
        ]
        leak_re = re.compile(
            r"原件|子代理|题解代理|intake-|work/|白名单|\bOCR\b|\b(?:048|049|03|19|20)_[A-Za-z0-9_\u4e00-\u9fff]+|\b(?:tma|ed|mpea|cva|cplx|real|prob|alg|stat|stoc|ode|pde)_[0-9a-f]{6,}\b"
        )
        for code in new_codes:
            for q in self.bank[code]:
                for txt in (q.stem_md, q.answer_md, q.solution_md, q.note or ""):
                    self.assertIsNone(leak_re.search(txt), f"Internal leak in {q.id}: {txt!r}")
        self.assertEqual(self.bank.get("022392-exam-2021f-m-01").source_exam_kind, "midterm")
        self.assertEqual(self.bank.get("022392-exam-2021f-f-01").source_exam_kind, "final")
        self.assertEqual(self.bank.get("022057-tb-01").answer_origin, "community")
        self.assertEqual(self.bank.get("001101-hw1-01").source_kind, "notes")
        self.assertEqual(self.bank.get("001122-hw1-01").source_kind, "notes")
        self.assertEqual(self.bank.get("011103-exam-2021s-f-01").source_year, 2021)
        self.assertEqual(self.bank.get("210045-exam-2025s-f-01").source_term, "2024-2025-2")
        self.assertEqual(self.bank.get("MATH1006-exam-2026m-01").answer_origin, "official")
