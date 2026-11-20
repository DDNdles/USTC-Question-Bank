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
| `001548` 复变函数B | `complex_b`, `complex_b_midterm` | `third_party_exam` | 中国科学技术大学《复变函数B》2003–2026 历年真题及公开参考答案；部分 2019–2020 答案源自 renyixin 公开文档；索引入口见 [USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation)、feixu 镜像、`ustcmathexam`、评课社区 (`icourse.club`) |
| `001548` 复变函数B | `jiangyi_examples` | `third_party_notes` | 舒文炫《复变函数B期末复习讲义》（第二版）例题 |
| `001548` 复变函数B | `github_workbook` | `third_party_community` | GitHub [`jieyou520/-`](https://github.com/jieyou520/-) 复变函数期末复习题库（原仓库无 LICENSE） |
| `001548` 复变函数B | `yan_complex` | `third_party_textbook` | 严镇军《复变函数》（第 2 版，中国科学技术大学出版社）第 1–9 章课后习题及书末部分参考答案 |
| `001548` 复变函数B | `yan_mp_part1`, `yan_mp_part2` | `third_party_textbook` | 严镇军《数学物理方法》（中国科学技术大学出版社）第一、二篇课后习题及书末部分参考答案 |
| `MATH1006` 数学分析(B1) | `ma1_exams` | `third_party_exam` | 中国科学技术大学《数学分析(B1)》2016–2025 历年小测/期中/期末真题及公开参考答案/评分细则 |
| `MATH1006` 数学分析(B1) | `ma1_textbook` | `third_party_textbook_and_community` | 程艺、陈卿、李平《数学分析讲义》第一册课后习题；非官方详解源自 GitHub [`DongYaoZe/math-analysis-lectures-solutions-USTC`](https://github.com/DongYaoZe/math-analysis-lectures-solutions-USTC)（原仓库无 LICENSE，按 `origin: "community"` 标注） |
| `MATH1007` 数学分析(B2) | `ma2_exams` | `third_party_exam` | 中国科学技术大学《数学分析(B2)》2018–2026 历年期中/期末真题及公开参考答案/评分细则 |
| `MATH1007` 数学分析(B2) | `ma2_textbook` | `third_party_textbook_and_community` | 程艺、陈卿、李平《数学分析讲义》第二册课后习题；非官方详解源自 GitHub [`DongYaoZe/math-analysis-lectures-solutions-USTC`](https://github.com/DongYaoZe/math-analysis-lectures-solutions-USTC)（原仓库无 LICENSE，按 `origin: "community"` 标注） |

## 3. Downstream Usage Responsibility

If you build downstream applications, datasets, or services on top of this repository:

- Filter by `source.rights` and `answer.origin` according to your compliance needs.
- Do not redistribute third-party textbook exercises or unlicensed community solutions under permissive/commercial terms without obtaining permission from the original rights holders.

## 4. Takedown & Attribution Requests

This repository is maintained strictly for non-commercial study, teaching reference, and academic tooling. If you are a copyright holder or original author and wish to update attribution or request removal of any specific batch or question:

1. Open an issue at <https://github.com/DDNdles/USTC-Question-Bank/issues> specifying the course code, batch (`source.batch`), or question IDs (`id`).
2. Verified takedown requests will be honored promptly by removing the affected entries and updating the repository history/releases as needed.
