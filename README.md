# USTC-Question-Bank

中国科学技术大学（USTC）本科课程结构化题库。每道题包含 Markdown + LaTeX 题干、答案、分步解析、知识点树标签、难度评级、出处与答案可信分级，设计目标是不只是「存题」，而是作为**标准化数据层与零依赖基础库**供刷题应用、LaTeX 组卷、Anki 制卡、RAG 检索与评测基准直接消费。

> **许可边界提示**：本仓库的代码、JSON Schema、知识点树、元数据与原创标注采用 [MIT License](LICENSE)；第三方真题、出版教材习题及引用解答的版权归原作者与出版社所有，**不适用 MIT**。详阅 [NOTICE.md](NOTICE.md)。

## 当前收录规模（v0.1.0）

| 课号 | 课程名 | 总题数 | `official` | `community` | `ai` | 低置信隔离 | 真题覆盖年份 | 知识点节点 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `001548` | 复变函数B | 571 | 229 | 26 | 316 | 7 | 2003–2025 | 35 |
| `MATH1006` | 数学分析(B1) | 445 | 133 | 300 | 12 | 0 | 2016–2025 | 31 |
| `MATH1007` | 数学分析(B2) | 569 | 131 | 438 | 0 | 0 | 2018–2026 | 28 |
| **合计** | **3 门课程** | **1,585** | **493** | **764** | **328** | **7** | — | **94** |

- 所有 1,585 题均包含完整题干、答案与分步解析，无空白项。
- `official`：原卷参考答案、评分细则或教材书末参考答案。
- `community`：非官方书面详解（如 `DongYaoZe`《数学分析讲义》详解、舒文炫讲义例题、renyixin 2019–2020 答案）。
- `ai`：无原始答案时由模型求解或入库独立推导/补证。

## 仓库结构

按中科大官方课号分目录组织，方便后续按相同契约持续扩展其他课程：

```text
USTC-Question-Bank/
├── manifest.json                 # 全库索引：课程列表、统计、路径与 SHA-256
├── schema/
│   ├── manifest.schema.json      # 索引契约（JSON Schema 2020-12）
│   ├── question.schema.json      # 单题契约
│   └── taxonomy.schema.json      # 知识点树契约
├── courses/
│   ├── 001548/                   # 复变函数B
│   │   ├── meta.json             # 课程元信息、批次清单、已知勘误说明
│   │   ├── taxonomy.json         # 知识点层次树
│   │   └── questions.jsonl       # 每行一道题（UTF-8，按稳定 ID 排序）
│   ├── MATH1006/                 # 数学分析(B1)
│   └── MATH1007/                 # 数学分析(B2)
├── python/ustc_qbank/            # 零第三方依赖 Python 加载库与 SQLite 构建器
├── types/index.d.ts              # TypeScript 类型定义
├── scripts/
│   ├── validate.py               # Schema、ID、kp 白名单、LaTeX 与 SHA-256 校验
│   └── build_sqlite.py           # 一键编译带 FTS5 全文索引的 SQLite 数据库
├── tests/test_library.py         # 单元测试
├── LICENSE                       # MIT License（仅限原创代码/架构/元数据）
└── NOTICE.md                     # 第三方来源署名、版权声明与侵删渠道
```

本仓库不提交扫描 PDF 原件、整本教材 OCR 原文或二进制 SQLite 文件；需要 SQLite 时通过 `scripts/build_sqlite.py` 本地一键构建（或从 Release 附件获取）。

## 单题数据契约

`courses/<course_code>/questions.jsonl` 每行是一条符合 [schema/question.schema.json](schema/question.schema.json) 的 JSON 对象：

```json
{
  "id": "001548-exam-2003f-01",
  "course_code": "001548",
  "schema_version": "1.0",
  "type": "blank",
  "stem": { "md": "设方程 $z^{3}=\\bar{z}$，求 $z$。" },
  "answer": {
    "md": "$z\\in\\{0,\\ 1,\\ -1,\\ \\mathrm{i},\\ -\\mathrm{i}\\}$",
    "origin": "ai",
    "origin_detail": "入库时独立推导"
  },
  "solution": {
    "md": "取模，$|z|^{3}=|z|$，故 $|z|=0$ 或 $|z|=1$。...",
    "steps": ["取模，$|z|^{3}=|z|$，故 $|z|=0$ 或 $|z|=1$。", "..."]
  },
  "tags": {
    "kp_ids": ["cplx.eq"],
    "keywords": ["复方程求解", "开方与对数方程"],
    "difficulty": 2
  },
  "source": {
    "kind": "exam_paper",
    "batch": "complex_b",
    "ref": "2003-2004学年第一学期复变函数（B）期末 第一(1)题",
    "year": 2003,
    "term": "2003-2004-1",
    "exam_kind": "final",
    "url": "https://share.feixu.site/数学类/复变函数/复变函数历年真题.pdf",
    "rights": "third_party_exam"
  },
  "quality": {
    "quarantined": false,
    "quarantine_reason": null,
    "confidence": null,
    "note": null,
    "overlap_hint": null
  }
}
```

### 字段约定

- **`id`**：全局唯一、稳定、URL 安全的确定性编号，格式 `<course_code>-<batch_slug>-<local_key>`（如 `MATH1006-tb-1.1.1`、`MATH1007-exam-2025f-03`），可安全用作数据库主键、路由参数或外部引用锚点。
- **`tags.kp_ids`**：受同目录 `taxonomy.json` 白名单约束，支持按父节点递归检索整个知识子树。
- **`quality.quarantined`**：`true` 表示题干存疑（如手写回忆版）或模型自评低置信；`Course.query()` 默认排除这些题目，可传 `exclude_quarantined=False` 显式包含。
- **`quality.overlap_hint`**：`001548` 中严镇军《数学物理方法》第一篇（`yan_mp_part1`）与《复变函数》（`yan_complex`）存在内容重叠，如需去重可直接过滤 `exclude_batches=["yan_mp_part1"]`。
- **`source.rights`**：标明每条题目的第三方权利分类，便于下游应用按需过滤（例如仅拉取 `third_party_exam`）。

## 作为库使用

### 1. Python（零第三方依赖）

克隆仓库后可直接安装或将其作为 git submodule 引入：

```bash
git clone https://github.com/DDNdles/USTC-Question-Bank.git
pip install -e ./USTC-Question-Bank
```

```python
from ustc_qbank import QuestionBank

bank = QuestionBank("./USTC-Question-Bank")

# 查看所有课程
print(bank.course_codes)  # ['001548', 'MATH1006', 'MATH1007']

# 按知识点父节点检索（自动展开 ma1.lim 下全部子节点）
ma1 = bank["MATH1006"]
limit_exams = ma1.query(
    kp="ma1.lim",
    source_kinds=["exam_paper"],
    origins=["official"],
    difficulty=(2, 4),
)

# 可复现随机抽题（自动排除低置信题，并排除复变教材重叠批次）
paper = bank["001548"].sample(
    12,
    seed=2026,
    origins=["official", "community"],
    exclude_batches=["yan_mp_part1"],
)

# 按全局 ID 精确查找
q = bank.get("MATH1007-exam-2026f-01")
print(q.stem_md)
```

### 2. 编译为 SQLite + FTS5 全文检索引擎

适合桌面端、后端服务或本地 CLI 刷题工具：

```bash
python scripts/build_sqlite.py -o dist/ustc-question-bank.sqlite
```

生成的数据库包含 `courses`、`taxonomy`、`questions`、`question_kp` 与 `questions_fts`（FTS5 `unicode61` 全文索引）：

```sql
SELECT q.id, q.source_ref, q.difficulty
FROM questions_fts f
JOIN questions q ON q.id = f.id
WHERE questions_fts MATCH 'Laurent OR 留数'
  AND q.quarantined = 0
LIMIT 10;
```

### 3. TypeScript / 前端 / 静态站直连

仓库提供 [types/index.d.ts](types/index.d.ts)，且 `manifest.json`、`taxonomy.json`、`questions.jsonl` 均可通过 GitHub Raw 或静态托管直接读取：

```ts
import type { Manifest, QuestionRecord } from "./types";

const BASE = "https://raw.githubusercontent.com/DDNdles/USTC-Question-Bank/main";
const manifest: Manifest = await fetch(`${BASE}/manifest.json`).then((r) => r.json());
const raw = await fetch(`${BASE}/${manifest.courses[0].paths.questions}`).then((r) => r.text());
const questions: QuestionRecord[] = raw
  .trim()
  .split("\n")
  .map((line) => JSON.parse(line));
```

### 4. AI Agent / RAG / 评测数据集

- **Agent 发现入口**：先读根目录 `manifest.json` 获取课程清单、统计与 SHA-256，再按需读取对应课程的 `taxonomy.json` 与 `questions.jsonl`。
- **Hugging Face `datasets`**：可直接按标准 JSONL 加载：`load_dataset("json", data_files="courses/MATH1006/questions.jsonl")`。

## 各课程批次明细

### `001548` 复变函数B（571 题）

| `source.batch` | 题数 | 说明 |
| --- | ---: | --- |
| `complex_b` | 225 | 2003–2026 年 14 套期末真题（含 2019–2020 补考） |
| `complex_b_midterm` | 3 | 2023 秋期中考试（Q1/Q5/Q6） |
| `jiangyi_examples` | 10 | 舒文炫《复变函数B期末复习讲义》（第二版）例题 |
| `github_workbook` | 40 | GitHub `jieyou520/-` 复变复习题库 |
| `yan_complex` | 127 | 严镇军《复变函数》（第 2 版）第 1–9 章习题 |
| `yan_mp_part1` | 99 | 严镇军《数学物理方法》第一篇第 1–7 章习题（与 `yan_complex` 部分重叠） |
| `yan_mp_part2` | 67 | 严镇军《数学物理方法》第二篇第 1–5 章习题 |

### `MATH1006` 数学分析(B1)（445 题）

| `source.batch` | 题数 | 说明 |
| --- | ---: | --- |
| `ma1_exams` | 145 | 2016 小测 + 2017–2025 学年期中/期末 18 套真题 |
| `ma1_textbook` | 300 | 《数学分析讲义》第一册第 1–7 章习题（详解源自 `DongYaoZe`，`origin=community`） |

### `MATH1007` 数学分析(B2)（569 题）

| `source.batch` | 题数 | 说明 |
| --- | ---: | --- |
| `ma2_exams` | 131 | 2018–2026 春季期中/期末 17 套真题 |
| `ma2_textbook` | 438 | 《数学分析讲义》第二册第 8–13 章习题（详解源自 `DongYaoZe`，`origin=community`） |

各课程的详细勘误与已知局限见对应 `courses/<course_code>/meta.json` 中的 `known_notes` 字段。

## 校验与开发

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

发现题干、答案或解析错误，请使用 [勘误 Issue 模板](.github/ISSUE_TEMPLATE/errata.yml) 反馈或直接提交 PR（参见 [CONTRIBUTING.md](CONTRIBUTING.md)）。

## 许可与致谢

- 仓库代码、Schema、知识点树、元数据及文档采用 [MIT License](LICENSE)。
- 第三方真题、出版教材习题及非官方解答版权归原权利人所有，详阅 [NOTICE.md](NOTICE.md)。
- 资料索引得益于 [TwinJades/USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation) 及历届整理与维护课程资料的中科大学长学姐。
