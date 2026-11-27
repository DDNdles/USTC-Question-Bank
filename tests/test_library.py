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
                "MATH1001",
                "MATH1002",
                "PHYS1001B",
                "PHYS1002B",
                "MATH1004",
                "MATH1005",
                "MATH1010",
                "PHYS1004H",
                "PHYS1004C",
                "PHYS1004B",
                "PHYS1001H",
                "019161",
                "019163",
                "019165",
                "019166",
                "CS1003L",
                "CS1002A",
                "MARX1012",
                "229001",
                "MATH1003",
                "MATH1008",
                "PHYS1005A",
                "PHYS1005B",
                "PHYS1003B",
                "MARX1011",
                "MARX1010",
                "MARX1013",
                "MARX1014",
                "009501",
                "PHYS1010",
                "019011",
                "019012",
                "019047",
                "022392",
                "022057",
                "001506",
                "001505",
                "MATH3008",
                "MATH3002",
                "MATH3007",
                "MATH3001",
                "017063",
                "017129",
                "001101",
                "001122",
                "MATH2004",
                "011103",
                "210045",
                "MATH2003",
                "MATH2001",
                "011146",
                "022148",
                "022062",
            ],
        )
        self.assertEqual(len(self.bank["001548"]), 571)
        self.assertEqual(len(self.bank["MATH1006"]), 554)
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
        self.assertEqual(len(self.bank["MATH1001"]), 169)
        self.assertEqual(len(self.bank["MATH1002"]), 299)
        self.assertEqual(len(self.bank["PHYS1001B"]), 379)
        self.assertEqual(len(self.bank["PHYS1002B"]), 277)
        self.assertEqual(len(self.bank["MATH1004"]), 171)
        self.assertEqual(len(self.bank["MATH1005"]), 166)
        self.assertEqual(len(self.bank["MATH1010"]), 131)
        self.assertEqual(len(self.bank["PHYS1004H"]), 131)
        self.assertEqual(len(self.bank["PHYS1004C"]), 151)
        self.assertEqual(len(self.bank["PHYS1004B"]), 151)
        self.assertEqual(len(self.bank["PHYS1001H"]), 78)
        self.assertEqual(len(self.bank["019161"]), 132)
        self.assertEqual(len(self.bank["019163"]), 86)
        self.assertEqual(len(self.bank["019165"]), 328)
        self.assertEqual(len(self.bank["019166"]), 252)
        self.assertEqual(len(self.bank["CS1003L"]), 191)
        self.assertEqual(len(self.bank["CS1002A"]), 232)
        self.assertEqual(len(self.bank["MARX1012"]), 1227)
        self.assertEqual(len(self.bank["229001"]), 431)
        self.assertEqual(len(self.bank["MATH1003"]), 247)
        self.assertEqual(len(self.bank["MATH1008"]), 270)
        self.assertEqual(len(self.bank["PHYS1005A"]), 165)
        self.assertEqual(len(self.bank["PHYS1005B"]), 156)
        self.assertEqual(len(self.bank["PHYS1003B"]), 147)
        self.assertEqual(len(self.bank["MARX1011"]), 511)
        self.assertEqual(len(self.bank["MARX1010"]), 1106)
        self.assertEqual(len(self.bank["MARX1013"]), 681)
        self.assertEqual(len(self.bank["MARX1014"]), 285)
        self.assertEqual(len(self.bank["009501"]), 236)
        self.assertEqual(len(self.bank["PHYS1010"]), 716)
        self.assertEqual(len(self.bank["019011"]), 1559)
        self.assertEqual(len(self.bank["019012"]), 99)
        self.assertEqual(len(self.bank["019047"]), 193)
        self.assertEqual(len(self.bank["022392"]), 293)
        self.assertEqual(len(self.bank["022057"]), 198)
        self.assertEqual(len(self.bank["001506"]), 182)
        self.assertEqual(len(self.bank["001505"]), 173)
        self.assertEqual(len(self.bank["MATH3008"]), 305)
        self.assertEqual(len(self.bank["MATH3002"]), 239)
        self.assertEqual(len(self.bank["MATH3007"]), 241)
        self.assertEqual(len(self.bank["MATH3001"]), 255)
        self.assertEqual(len(self.bank["017063"]), 84)
        self.assertEqual(len(self.bank["017129"]), 204)
        self.assertEqual(len(self.bank["001101"]), 141)
        self.assertEqual(len(self.bank["001122"]), 103)
        self.assertEqual(len(self.bank["MATH2004"]), 241)
        self.assertEqual(len(self.bank["011103"]), 120)
        self.assertEqual(len(self.bank["210045"]), 140)
        self.assertEqual(len(self.bank["MATH2003"]), 67)
        self.assertEqual(len(self.bank["MATH2001"]), 567)
        self.assertEqual(len(self.bank["011146"]), 340)
        self.assertEqual(len(self.bank["022148"]), 687)
        self.assertEqual(len(self.bank["022062"]), 306)
        self.assertEqual(len(self.bank.all_questions()), 23507)
        self.assertEqual(len(self.bank.all_questions(exclude_quarantined=True)), 23201)

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

        q_ma1a = self.bank.get("MATH1001-exam-2026f-m-01")
        self.assertEqual(q_ma1a.course_code, "MATH1001")
        self.assertEqual(q_ma1a.answer_origin, "official")
        self.assertEqual(q_ma1a.source_term, "2026-2027-1")

        q_ma1c = self.bank.get("MATH1001-exam-2018f-f-01")
        self.assertEqual(q_ma1c.course_code, "MATH1001")
        self.assertEqual(q_ma1c.answer_origin, "community")

        q_ma2 = self.bank.get("MATH1002-exam-2020s-quiz-01")
        self.assertEqual(q_ma2.course_code, "MATH1002")
        self.assertEqual(q_ma2.answer_origin, "ai")
        self.assertEqual(q_ma2.source_year, 2020)
        self.assertEqual(q_ma2.source_term, "2019-2020-2")

        q_mb = self.bank.get("PHYS1001B-exam-2018-f-03")
        self.assertEqual(q_mb.course_code, "PHYS1001B")
        self.assertEqual(q_mb.answer_origin, "community")
        self.assertEqual(len(q_mb.stem_figures), 1)

        q_tb = self.bank.get("PHYS1002B-exam-2022s-f-06")
        self.assertEqual(q_tb.course_code, "PHYS1002B")
        self.assertEqual(q_tb.answer_origin, "official")
        self.assertEqual(len(q_tb.stem_figures), 1)
        self.assertEqual(len(q_tb.solution_figures), 1)

        q_laa1 = self.bank.get("MATH1004-exam-2018s-m-01")
        self.assertEqual(q_laa1.course_code, "MATH1004")
        self.assertEqual(q_laa1.answer_origin, "ai")
        self.assertEqual(q_laa1.source_term, "2017-2018-2")

        q_laa2 = self.bank.get("MATH1005-exam-2025f-f-01")
        self.assertEqual(q_laa2.course_code, "MATH1005")
        self.assertEqual(q_laa2.type, "multi")
        self.assertEqual(q_laa2.answer_origin, "official")
        self.assertGreaterEqual(len(q_laa2.options), 4)

        q_lab2 = self.bank.get("MATH1010-exam-2021f-m-01")
        self.assertEqual(q_lab2.course_code, "MATH1010")
        self.assertEqual(q_lab2.answer_origin, "official")
        self.assertEqual(q_lab2.source_term, "2021-2022-1")

        q_lab2_c = self.bank.get("MATH1010-exam-2024f-f2-01")
        self.assertEqual(q_lab2_c.course_code, "MATH1010")
        self.assertEqual(q_lab2_c.answer_origin, "community")

        q_emh = self.bank.get("PHYS1004H-exam-2024s-m2-07")
        self.assertEqual(q_emh.course_code, "PHYS1004H")
        self.assertEqual(q_emh.answer_origin, "official")
        self.assertEqual(len(q_emh.stem_figures), 1)
        self.assertEqual(len(q_emh.solution_figures), 1)

        q_emc = self.bank.get("PHYS1004C-exam-2022f-f-15")
        self.assertEqual(q_emc.course_code, "PHYS1004C")
        self.assertEqual(q_emc.answer_origin, "community")
        self.assertEqual(len(q_emc.stem_figures), 1)
        self.assertEqual(len(q_emc.solution_figures), 1)

        q_emb = self.bank.get("PHYS1004B-exam-2021s-m-01")
        self.assertEqual(q_emb.course_code, "PHYS1004B")
        self.assertEqual(q_emb.answer_origin, "official")
        self.assertEqual(len(q_emb.stem_figures), 1)
        self.assertEqual(len(q_emb.solution_figures), 1)

        q_mh = self.bank.get("PHYS1001H-exam-2023f-f-10")
        self.assertEqual(q_mh.course_code, "PHYS1001H")
        self.assertEqual(q_mh.answer_origin, "official")
        self.assertEqual(len(q_mh.stem_figures), 1)

        q_cpa = self.bank.get("019161-exam-2024f-f-32")
        self.assertEqual(q_cpa.course_code, "019161")
        self.assertEqual(len(q_cpa.stem_figures), 1)

        q_cpb = self.bank.get("019163-sol-c1014-01")
        self.assertEqual(q_cpb.course_code, "019163")
        self.assertEqual(q_cpb.answer_origin, "official")

        q_gnc = self.bank.get("019165-ex-13.16")
        self.assertEqual(q_gnc.course_code, "019165")
        self.assertEqual(q_gnc.answer_origin, "official")
        self.assertEqual(len(q_gnc.stem_figures), 1)
        self.assertEqual(len(q_gnc.solution_figures), 1)

        q_ino = self.bank.get("019166-drill-tut1-08")
        self.assertEqual(q_ino.course_code, "019166")
        self.assertEqual(len(q_ino.stem_figures), 1)

        q_cpl = self.bank.get("CS1003L-exam-2025f-quiz-01")
        self.assertEqual(q_cpl.course_code, "CS1003L")
        self.assertEqual(q_cpl.answer_origin, "official")

        q_csa = self.bank.get("CS1002A-exam-2020f-m-11")
        self.assertEqual(q_csa.course_code, "CS1002A")
        self.assertEqual(q_csa.answer_origin, "ai")
        self.assertEqual(len(q_csa.stem_figures), 1)

        q_marx = self.bank.get("MARX1012-exam-2022-f-01")
        self.assertEqual(q_marx.course_code, "MARX1012")
        self.assertEqual(q_marx.answer_origin, "community")

        q_dm = self.bank.get("229001-sol-combi-14")
        self.assertEqual(q_dm.course_code, "229001")
        self.assertEqual(q_dm.answer_origin, "official")
        self.assertEqual(len(q_dm.stem_figures), 1)

        q_ma3 = self.bank.get("MATH1003-exam-2016f-f-01")
        self.assertEqual(q_ma3.course_code, "MATH1003")
        self.assertEqual(q_ma3.answer_origin, "ai")
        self.assertEqual(q_ma3.source_year, 2016)

        q_mb3 = self.bank.get("MATH1008-exam-2016f-f-01")
        self.assertEqual(q_mb3.course_code, "MATH1008")
        self.assertEqual(q_mb3.answer_origin, "official")
        self.assertEqual(q_mb3.source_year, 2016)

        q_apa = self.bank.get("PHYS1005A-exam-2016-f-01")
        self.assertEqual(q_apa.course_code, "PHYS1005A")
        self.assertEqual(q_apa.answer_origin, "official")
        self.assertEqual(q_apa.source_year, 2016)

        q_apb = self.bank.get("PHYS1005B-exam-2016s-f-19")
        self.assertEqual(q_apb.course_code, "PHYS1005B")
        self.assertEqual(q_apb.answer_origin, "official")
        self.assertEqual(len(q_apb.solution_figures), 1)

        q_ob = self.bank.get("PHYS1003B-exam-2022s-f-09")
        self.assertEqual(q_ob.course_code, "PHYS1003B")
        self.assertEqual(q_ob.answer_origin, "ai")
        self.assertEqual(len(q_ob.stem_figures), 1)

        q_marxp = self.bank.get("MARX1011-exam-undated-f-01")
        self.assertEqual(q_marxp.course_code, "MARX1011")
        self.assertEqual(q_marxp.answer_origin, "ai")

        q_mch = self.bank.get("MARX1010-debate-001")
        self.assertEqual(q_mch.course_code, "MARX1010")
        self.assertEqual(q_mch.answer_origin, "official")

        q_mg = self.bank.get("MARX1013-tb-001")
        self.assertEqual(q_mg.course_code, "MARX1013")
        self.assertEqual(q_mg.answer_origin, "official")

        q_xg = self.bank.get("MARX1014-exam-2022f-f-01")
        self.assertEqual(q_xg.course_code, "MARX1014")
        self.assertEqual(q_xg.answer_origin, "ai")
        self.assertEqual(q_xg.source_year, 2022)

        q_ed = self.bank.get("009501-mock-01")
        self.assertEqual(q_ed.course_code, "009501")
        self.assertEqual(q_ed.answer_origin, "official")
        self.assertEqual(len(q_ed.stem_figures), 1)
        self.assertEqual(len(q_ed.solution_figures), 1)

        q_qp = self.bank.get("PHYS1010-exam-2023-f-01")
        self.assertEqual(q_qp.course_code, "PHYS1010")
        self.assertEqual(q_qp.answer_origin, "ai")
        self.assertEqual(q_qp.source_year, 2023)

        q_oca1 = self.bank.get("019011-exam-2013f-f-01")
        self.assertEqual(q_oca1.course_code, "019011")
        self.assertEqual(q_oca1.answer_origin, "ai")
        self.assertEqual(q_oca1.source_year, 2013)

        q_oca2 = self.bank.get("019012-exam-2017s-f-01")
        self.assertEqual(q_oca2.course_code, "019012")
        self.assertEqual(q_oca2.answer_origin, "ai")
        self.assertEqual(q_oca2.source_year, 2017)

        q_ocb = self.bank.get("019047-exam-2021f-quiz1-01")
        self.assertEqual(q_ocb.course_code, "019047")
        self.assertEqual(q_ocb.answer_origin, "official")
        self.assertEqual(q_ocb.source_year, 2021)

        for qid, code, origin, year in [
            ("022392-exam-2016f-f-01", "022392", "official", 2016),
            ("022057-tb-01", "022057", "community", None),
            ("001506-exam-2001f-f-01", "001506", "ai", 2001),
            ("001505-exam-2005-f-01", "001505", "ai", 2005),
            ("MATH3008-exam-2011-f-01", "MATH3008", "ai", 2011),
            ("MATH3002-hw-01", "MATH3002", "official", None),
            ("MATH3007-exam-2023-m-01", "MATH3007", "official", 2023),
            ("MATH3001-exam-2023-f-01", "MATH3001", "official", 2023),
            ("017063-exam-2021-m-01", "017063", "ai", 2021),
            ("017129-exam-2011-m-01", "017129", "ai", 2011),
            ("001101-exam-2016-m-01", "001101", "ai", 2016),
            ("001122-exam-2020-f-01", "001122", "ai", 2020),
            ("MATH2004-exam-2025-f-01", "MATH2004", "official", 2025),
            ("011103-exam-2026s-f-01", "011103", "ai", 2026),
            ("210045-exam-2025s-f-01", "210045", "official", 2025),
            ("MATH2003-exam-2024-m-01", "MATH2003", "official", 2024),
            ("MATH2001-exam-2006s-f-01", "MATH2001", "ai", 2006),
            ("011146-hw-01", "011146", "official", None),
            ("022148-tb-v1-01", "022148", "official", None),
            ("022062-exam-2016s-f-01", "022062", "official", 2016),
        ]:
            qn = self.bank.get(qid)
            self.assertEqual(qn.course_code, code)
            self.assertEqual(qn.answer_origin, origin)
            self.assertEqual(qn.source_year, year)

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
            ("PHYS1001B", 145, 143),
            ("PHYS1002B", 30, 30),
            ("PHYS1004H", 37, 36),
            ("PHYS1004C", 98, 92),
            ("PHYS1004B", 64, 64),
            ("PHYS1001H", 14, 13),
            ("019161", 4, 4),
            ("019165", 5, 5),
            ("019166", 1, 1),
            ("CS1002A", 54, 54),
            ("229001", 3, 3),
            ("PHYS1005B", 3, 3),
            ("PHYS1003B", 23, 23),
            ("009501", 70, 70),
            ("019011", 186, 186),
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
                self.assertEqual(count, 23507)
                hits = conn.execute(
                    "SELECT id FROM questions_fts WHERE questions_fts MATCH 'Laurent' LIMIT 5"
                ).fetchall()
                self.assertGreater(len(hits), 0)
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
