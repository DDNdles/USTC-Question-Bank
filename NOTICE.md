# Copyright Notice & Third-Party Attribution

## 1. License Boundary

The **MIT License** in [`LICENSE`](LICENSE) applies **only** to the original works authored for this repository:

- Data schemas (`schema/*.json`) and TypeScript definitions (`types/index.d.ts`)
- Python library (`python/ustc_qbank/`) and build/validation scripts (`scripts/`)
- Course metadata (`manifest.json`, `courses/*/meta.json`), knowledge point taxonomies (`courses/*/taxonomy.json`), difficulty/keyword annotations, and repository documentation
- Original or AI-assisted solutions marked with `"origin": "ai"`

The MIT License **does NOT apply** to third-party exam questions, textbook exercises, official reference answers, lecture notes, or community solutions indexed in `courses/*/questions.jsonl`. Copyright for those materials remains strictly with their respective authors, instructors, institutions, and publishers.

This repository does **not** host scanned textbook PDFs, raw exam PDFs, or full-book OCR dumps.

## 2. Third-Party Sources & Attributions

| Course | Batch (`source.batch`) | Rights Class | Original Source / Attribution |
| --- | --- | --- | --- |
| `001548` 复变函数B | `complex_b`, `complex_b_midterm` | `third_party_exam` | 中国科学技术大学《复变函数B》2003–2026 历年真题及公开参考答案；部分 2019–2020 答案源自 renyixin 公开文档；索引入口见 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[feixu 镜像](https://share.feixu.site/)、[ustcmathexam](https://ustcmathexam.github.io/)、[评课社区](https://icourse.club/) |
| `001548` 复变函数B | `jiangyi_examples` | `third_party_notes` | 舒文炫《复变函数B期末复习讲义》（第二版）例题（源自 [feixu 镜像](https://share.feixu.site/)） |
| `001548` 复变函数B | `github_workbook` | `third_party_community` | GitHub [`jieyou520/-`](https://github.com/jieyou520/-) 复变函数期末复习题库（原仓库无 LICENSE） |
| `001548` 复变函数B | `yan_complex` | `third_party_textbook` | 严镇军《复变函数》（第 2 版，中国科学技术大学出版社）第 1–9 章课后习题及书末部分参考答案 |
| `001548` 复变函数B | `yan_mp_part1`, `yan_mp_part2` | `third_party_textbook` | 严镇军《数学物理方法》（中国科学技术大学出版社）第一、二篇课后习题及书末部分参考答案 |
| `MATH1006` 数学分析(B1) | `ma1_exams` | `third_party_exam` | 中国科学技术大学《数学分析(B1)》2016–2025 历年小测/期中/期末真题及公开参考答案/评分细则（源自 [feixu 镜像](https://share.feixu.site/)、[ustcmathexam](https://ustcmathexam.github.io/)、[Passiflora-sago](https://github.com/Passiflora-sago/Passiflora-sago.github.io)） |
| `MATH1006` 数学分析(B1) | `ma1_textbook` | `third_party_textbook_and_community` | 程艺、陈卿、李平《数学分析讲义》第一册课后习题；非官方详解源自 GitHub [`DongYaoZe/math-analysis-lectures-solutions-USTC`](https://github.com/DongYaoZe/math-analysis-lectures-solutions-USTC)（原仓库无 LICENSE，按 `origin: "community"` 标注） |
| `MATH1007` 数学分析(B2) | `ma2_exams` | `third_party_exam` | 中国科学技术大学《数学分析(B2)》2018–2026 历年期中/期末真题及公开参考答案/评分细则（源自 [feixu 镜像](https://share.feixu.site/)、[ustcmathexam](https://ustcmathexam.github.io/)） |
| `MATH1007` 数学分析(B2) | `ma2_textbook` | `third_party_textbook_and_community` | 程艺、陈卿、李平《数学分析讲义》第二册课后习题；非官方详解源自 GitHub [`DongYaoZe/math-analysis-lectures-solutions-USTC`](https://github.com/DongYaoZe/math-analysis-lectures-solutions-USTC)（原仓库无 LICENSE，按 `origin: "community"` 标注） |
| `MATH1009` 线性代数(B1) | `la1_exams` | `third_party_exam` | 中国科学技术大学《线性代数(B1)》2010–2026 学年 42 套期中/期末真题及参考答案；其中花开花败《线性代数B1历年真题及参考解答》（2024-07，20 套，线代 B1 助教编写）按 `origin: "community"` 标注；来源包括 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[ustcmathexam](https://ustcmathexam.github.io/)、[feixu 镜像](https://share.feixu.site/)、[评课社区](https://icourse.club/)、[`fandahao17/USTC-CS-Courses-Resource`](https://github.com/fandahao17/USTC-CS-Courses-Resource)、[`Wloner0809/ustc-course-resource`](https://github.com/Wloner0809/ustc-course-resource) |
| `MATH1009` 线性代数(B1) | `la1_textbook` | `third_party_textbook` | 李尚志《线性代数学习指导》（中国科学技术大学出版社）第 1–4、6、8、9 章例题分析与解答 |
| `CS1003` 计算机程序设计 | `cs1_exams` | `third_party_exam` | 中国科学技术大学《计算机程序设计》（C 语言，CS1003 / CS1003L）2018–2025 年 13 套期中/期末/补考/机考真题及参考答案；sxl 手写答案、评课社区详细解析及 duxiaoyang 修订答案按 `origin: "community"` 标注；来源包括 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[feixu 镜像](https://share.feixu.site/)、[`guch8017/USTC_CS_EXAM`](https://github.com/guch8017/USTC_CS_EXAM)、[`duxiaoyang/USTC-Course-Materials`](https://github.com/duxiaoyang/USTC-Course-Materials)、[评课社区](https://icourse.club/) |
| `CS1003` 计算机程序设计 | `cs1_quiz` | `third_party_textbook` | 《计算机程序设计学习指导与实践》（2012 版）综合测试题 4 套、2024 秋模拟测试 4 套及 2025 版复习测试 4 套（源自 [feixu 镜像](https://share.feixu.site/)、[`duxiaoyang/USTC-Course-Materials`](https://github.com/duxiaoyang/USTC-Course-Materials)） |
| `CS1003` 计算机程序设计 | `cs1_banks` | `third_party_community` | 公开 C 语言题库（《C语言程序设计》试题集 2009 版、理论上机选择 200+45 题、分类选择题库，源自 [feixu 镜像](https://share.feixu.site/)） |
| `CS1003` 计算机程序设计 | `cs1_drill` | `third_party_notes` | 指针专题练习、期中练习（含 sxl 手写答案，按 `origin: "community"` 标注）、L 班习题课与期末上机习题课课件（源自 [feixu 镜像](https://share.feixu.site/)、[`duxiaoyang/USTC-Course-Materials`](https://github.com/duxiaoyang/USTC-Course-Materials)、[评课社区](https://icourse.club/)） |
| `PHYS1001A` 力学A | `mech1_exams`, `mech1_quiz` | `third_party_exam` | 中国科学技术大学《力学A》（PHYS1001A / A(L)）2005–2026 学年期中/期末真题、力学历年考题合集及公开参考答案，含配图裁剪（源自 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[ustcphyexam](https://ustcphyexam.github.io/)、[feixu 镜像](https://share.feixu.site/)、[评课社区](https://icourse.club/)） |
| `PHYS1001A` 力学A | `mech1_drill` | `third_party_notes` | 刚体笔记整理例题及自带解法（按 `origin: "community"` 标注，源自 [评课社区](https://icourse.club/)） |
| `PHYS1002A` 热学A | `therm1_exams`, `therm1_quiz`, `therm1_drill` | `third_party_exam` / `third_party_textbook_and_community` / `third_party_notes` | 中国科学技术大学《热学A》（PHYS1002A）2004–2026 年期中/期末/预考/免修考与三次小测真题、热学历年真题合订本、2023 春 wxf 班参考题及清华大学《大学物理》习题库·热学（源自 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[ustcphyexam](https://ustcphyexam.github.io/)、[feixu 镜像](https://share.feixu.site/)、[评课社区](https://icourse.club/)） |
| `PHYS1004A` 电磁学A | `em1_exams`, `em1_quiz`, `em1_drill` | `third_party_exam` / `third_party_notes` | 中国科学技术大学《电磁学A》（PHYS1004A）2017–2026 年期中/期末公共题、秦敢期中样题、各班期中期末回忆版、课堂小测及磁场习题课讲稿例题（源自 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[ustcphyexam](https://ustcphyexam.github.io/)、[feixu 镜像](https://share.feixu.site/)、[评课社区](https://icourse.club/)） |
| `210070` 数据结构及其算法 | `ds1_exams`, `ds1_drill` | `third_party_exam` / `third_party_notes` | 中国科学技术大学《数据结构及其算法》（210070 / CS2502A）2008–2024 年期末真题、《数据结构》试卷A、四学年答案汇编（[`ly382965/USTC_learning_materials`](https://github.com/ly382965/USTC_learning_materials)，按 `origin: "community"` 标注）、2-4-6-8 / 3-5-7-9 / 10.24 习题课讲义及六次课程作业（源自 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[feixu 镜像](https://share.feixu.site/)、[`guch8017/USTC_CS_EXAM`](https://github.com/guch8017/USTC_CS_EXAM)、[`li-qi-lin/USTC-Course-Materials-Sharing`](https://github.com/li-qi-lin/USTC-Course-Materials-Sharing)、[评课社区](https://icourse.club/)） |
| `STAT2002` 概率论与数理统计 | `stat1_exams` | `third_party_exam` | 中国科学技术大学《概率论与数理统计》（STAT2002）2002–2026 学年共 36 套期中/期末真题及卷内/合集参考答案（源自 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[ustcphyexam](https://ustcphyexam.github.io/)、[ustcmathexam](https://ustcmathexam.github.io/)、[feixu 镜像](https://share.feixu.site/)、[`guch8017/USTC_CS_EXAM`](https://github.com/guch8017/USTC_CS_EXAM)、`guidongnan` 与 [`li-qi-lin/USTC-Course-Materials-Sharing`](https://github.com/li-qi-lin/USTC-Course-Materials-Sharing)） |
| `PHYS1003A` 光学A | `opt1_exams` | `third_party_exam` | 中国科学技术大学《光学A》（PHYS1003A）2020–2026 学年 6 套期末/模拟试卷（含 2023 秋卷面手写批注答案版，按 `origin: "community"` 标注），来源包括 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[ustcphyexam](https://ustcphyexam.github.io/)、[feixu 镜像](https://share.feixu.site/) 与 [评课社区](https://icourse.club/) |
| `PHYS1003A` 光学A | `opt1_drills`, `opt1_sets` | `third_party_textbook` | 《光学复习指导》（第 1–7 章例题与作业题）及《光学A习题集》（源自 [评课社区](https://icourse.club/)） |
| `210050` 数字逻辑电路 | `dl1_exams` | `third_party_exam` | 中国科学技术大学《数字逻辑电路》（210050）2015–2023 学年 7 套期末真题与 2020 秋 06 班模拟卷（含 2019–2020 与 2020–2021 助教手写答案版，按 `origin: "community"` 标注）；来源包括 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[`guch8017/USTC_CS_EXAM`](https://github.com/guch8017/USTC_CS_EXAM)、[`li-qi-lin/USTC-Course-Materials-Sharing`](https://github.com/li-qi-lin/USTC-Course-Materials-Sharing) 与 [feixu 镜像](https://share.feixu.site/) |
| `210050` 数字逻辑电路 | `dl2_book`, `dl2_papers` | `third_party_textbook` | 《数字电子技术基础（第六版）学习辅导与习题解答》（阎石、王红编，高等教育出版社，2016）第二至第四部分第 1–8 章例题（66 题）、教材习题解答（227 题）与 7 套自测试卷及答案（127 题） |
| `023181` 线性电子线路 | `le1_book` | `third_party_textbook` | 《模拟电子技术基础（第五版）全程辅导与习题全解》（童诗白、华成英主编，清华大学电子学教研组编，高等教育出版社）第 1–10 章全部 342 道例题、自测题与课后习题（部分随文插图补自原教材第五版） |
| `023181` 线性电子线路 | `le1_exams` | `third_party_exam` | 中国科学技术大学《线性电子线路》（023181）2014–2019 年等 6 套期末真题/回忆版及 B 课样卷/模拟卷；来源包括 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[`EpiHio/USTC_Automation`](https://github.com/EpiHio/USTC_Automation)、[`Mr-Philo/USTC_EEIS_Courses`](https://github.com/Mr-Philo/USTC_EEIS_Courses) 与 [`li-qi-lin/USTC-Course-Materials-Sharing`](https://github.com/li-qi-lin/USTC-Course-Materials-Sharing) |
| `EE2003` 计算机原理与嵌入式系统 | `ce_book` | `third_party_textbook` | 胡访宇主编、王嵩/陈晓辉副主编《计算机原理与嵌入式系统》（中国科学技术大学出版社）第 1–8 章全部 295 道章末习题；部分题附 2025 版及旧版 52 页课程作业参考答案、第 8 章解析与第 1–5 章习题课讲义解答 |
| `EE2003` 计算机原理与嵌入式系统 | `ce_supp` | `third_party_notes` | 《计算机原理与嵌入式系统》课程作业参考答案教师加编补充选择题（24 题，源自 [`EpiHio/USTC_Automation`](https://github.com/EpiHio/USTC_Automation) 与 [share.feixu.site](https://share.feixu.site/)） |
| `EE2003` 计算机原理与嵌入式系统 | `ce_papers` | `third_party_exam` | 中国科学技术大学《计算机原理与嵌入式系统》（EE2003）2019–2020 A 卷、2023–2024 期末、2024 A 卷及 2023–2024 题型示意卷共 4 套；来源包括 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、[`EpiHio/USTC_Automation`](https://github.com/EpiHio/USTC_Automation)、[share.feixu.site](https://share.feixu.site/) 与 [评课社区](https://icourse.club/) |

## 3. Downstream Usage Responsibility

If you build downstream applications, datasets, or services on top of this repository:

- Filter by `source.rights` and `answer.origin` according to your compliance needs.
- Do not redistribute third-party textbook exercises or unlicensed community solutions under permissive/commercial terms without obtaining permission from the original rights holders.

## 4. Takedown & Attribution Requests

This repository is maintained strictly for non-commercial study, teaching reference, and academic tooling. If you are a copyright holder or original author and wish to update attribution or request removal of any specific batch or question:

1. Open an issue at <https://github.com/DDNdles/USTC-Question-Bank/issues> specifying the course code, batch (`source.batch`), or question IDs (`id`).
2. Verified takedown requests will be honored promptly by removing the affected entries and updating the repository history/releases as needed.
