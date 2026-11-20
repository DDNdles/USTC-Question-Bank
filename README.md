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

- **100% 带答案与分步解析**：全部 1,585 题均包含最终答案（`answer.md`）与完整解析（`solution.md` / `solution.steps`），无空白题。
- `official`：原卷参考答案、评分细则或教材书末参考答案。
- `community`：非官方书面详解（如 `DongYaoZe`《数学分析讲义》详解、舒文炫讲义例题、renyixin 2019–2020 答案）。
- `ai`：无原始答案时由模型求解或入库独立推导/补证。

## 仓库结构与可扩展性

按中科大官方课号分目录组织，面向全校本科课程持续扩展：

```text
USTC-Question-Bank/
├── manifest.json                 # 全库索引：课程列表、统计、路径、asset_base_url 与 SHA-256
├── schema/
│   ├── manifest.schema.json      # 索引契约（JSON Schema 2020-12）
│   ├── question.schema.json      # 单题契约（原生支持图片 figures 与选择题 options）
│   └── taxonomy.schema.json      # 知识点树契约
├── courses/
│   ├── 001548/                   # 复变函数B
│   │   ├── meta.json             # 课程元信息、批次清单、已知勘误说明
│   │   ├── taxonomy.json         # 知识点层次树
│   │   ├── questions.jsonl       # 每行一道题（UTF-8，按稳定 ID 排序）
│   │   └── assets/               # （按需创建）带图题的 SVG / WebP / PNG 配图
│   ├── MATH1006/                 # 数学分析(B1)
│   └── MATH1007/                 # 数学分析(B2)
├── python/ustc_qbank/            # 零第三方依赖 Python 加载库与 SQLite 构建器
├── types/index.d.ts              # TypeScript 类型定义
├── scripts/
│   ├── validate.py               # Schema、ID、kp 白名单、图片资产、LaTeX 与 SHA-256 校验
│   └── build_sqlite.py           # 一键编译带 FTS5 全文索引的 SQLite 数据库
├── tests/test_library.py         # 单元测试
├── LICENSE                       # MIT License（仅限原创代码/架构/元数据）
└── NOTICE.md                     # 第三方来源署名、版权声明与侵删渠道
```

### 面向全校规模与带图题的架构设计

- **按课分片、纯文本入库**：每门课独立 `courses/<课号>/questions.jsonl`，即使扩展到上百门课、数万道题，单文件与仓库压缩体积依然远低于 GitHub 上限。
- **不把 SQLite 与扫描件塞进 Git**：二进制 SQLite（带 FTS5 索引）通过 `scripts/build_sqlite.py` 本地一键生成或通过 GitHub Releases 分发，避免仓库历史膨胀。
- **原生支持带图题与选择题**：`stem`、`answer`、`solution` 与 `options[]` 均内置 `figures` 数组，支持 `courses/<课号>/assets/` 下的 `.svg`（首选矢量图）、`.webp`、`.png` 配图（单图限 500 KB，CI 自动校验引用完整性与防孤儿图）；当未来全校图片总量扩大时，只需在 `manifest.json` 配置 `asset_base_url` 指向外部对象存储/CDN（如 Cloudflare R2 或独立资产仓），无需修改任何题库 JSONL 或下游调用代码。

## 单题数据契约

`courses/<course_code>/questions.jsonl` 每行是一条符合 [schema/question.schema.json](schema/question.schema.json) 的 JSON 对象：

```json
{
  "id": "001548-exam-2003f-01",
  "course_code": "001548",
  "schema_version": "1.0",
  "type": "blank",
  "stem": {
    "md": "设方程 $z^{3}=\\bar{z}$，求 $z$。",
    "figures": []
  },
  "options": [],
  "answer": {
    "md": "$z\\in\\{0,\\ 1,\\ -1,\\ \\mathrm{i},\\ -\\mathrm{i}\\}$",
    "figures": [],
    "origin": "ai",
    "origin_detail": "入库时独立推导"
  },
  "solution": {
    "md": "取模，$|z|^{3}=|z|$，故 $|z|=0$ 或 $|z|=1$。...",
    "steps": ["取模，$|z|^{3}=|z|$，故 $|z|=0$ 或 $|z|=1$。", "..."],
    "figures": []
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
- **`stem.figures` / `answer.figures` / `solution.figures`**：每张图包含 `id`、`path`（相对路径 `assets/*.svg|webp|png`）、`alt`，可选 `caption`、`width`、`height`、`sha256`。
- **`options`**：选择题选项数组（`{ key, md, figures? }`），填空/解答/证明题为空数组 `[]`。
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

# 按全局 ID 精确查找 & 解析带图题资产路径（兼容本地与外置 CDN）
q = bank.get("MATH1007-exam-2026f-01")
print(q.stem_md)
for fig in q.stem_figures:
    print(bank[q.course_code].resolve_asset(fig.path))
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

## 加入共建 / 寻找 Contributor

这个仓库的长期目标是覆盖中科大尽可能多的本科核心课程（数分、线代、概率、大物、数理方法、专业课等），靠一个人很难维护全校所有课程的录入与校对。**非常欢迎中科大的同学、校友以及任何愿意帮忙的朋友成为 Contributor：**

- **认领一门课**：整理你正在学或刚考完的课程真题/习题（哪怕先交 1 套结构化真题也很棒）。
- **随手勘误**：刷题时发现 OCR 错字、LaTeX 符号偏差或答案有误，直接提 [勘误 Issue](.github/ISSUE_TEMPLATE/errata.yml) 或 PR。
- **核对存疑题**：帮忙核对 `quarantined: true` 的低置信/手写回忆题。
- **绘制题图**：给带图题目绘制清晰的 SVG / WebP 配图。
- **共建生态**：基于本库开发刷题网站、Anki 制卡脚本、组卷工具或 Agent 插件，欢迎在 README 展示你的项目。

具体格式要求和校验命令见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 联系方式

- **维护者 GitHub**：[@DDNdles](https://github.com/DDNdles)
- **勘误 / 新课程认领**：直接在 [GitHub Issues](https://github.com/DDNdles/USTC-Question-Bank/issues) 开帖（推荐，公开可追溯）
- **其他联系方式**：<!-- 如需补充公开邮箱 / QQ 群 / 微信，可在此处填写 -->

## 校验与开发

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

## 许可与致谢

- 仓库代码、Schema、知识点树、元数据及文档采用 [MIT License](LICENSE)。
- 第三方真题、出版教材习题及非官方解答版权归原权利人所有，详阅 [NOTICE.md](NOTICE.md)。
- 资料索引得益于 [TwinJades/USTC_Study_Materials_Navigation](https://github.com/TwinJades/USTC_Study_Materials_Navigation) 及历届整理与维护课程资料的中科大学长学姐。
