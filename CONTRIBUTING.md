# Contributing

欢迎所有中科大同学、校友以及对开放题库感兴趣的开发者加入共建！无论是一道题的符号勘误、补录一套新年份试卷，还是认领一门新课程的录入，都非常有价值。

## 我们可以一起做什么

- **题目与答案勘误**：修正题干 OCR 误差、LaTeX 排版问题、原卷/社区解答的数学错误。
- **补录新课程**：按统一 Schema 录入中科大其他本科课程（如线性代数、概率论与数理统计、大学物理、数据结构等）。
- **低置信题核对**：核对 `quality.quarantined = true` 的题目（如手写回忆版）并补充可靠出处。
- **带图题配图**：用 SVG（首选）或 WebP 重绘电路图、几何图、函数示意图等。
- **下游生态**：基于本库构建刷题网站、Anki 牌组、LaTeX 组卷工具或 AI 评测集。

## 基本规则

1. **严禁提交原始扫描件与大体积二进制文件**：禁止提交 `.pdf`、`.jpg`、`.jpeg`、`.sqlite`、`.zip`、`.rar` 或整本教材 OCR 原文。
2. **题图资产规范（支持带图题）**：
   - 图片统一存放在 `courses/<course_code>/assets/` 目录下，格式仅限 **`.svg`（矢量图首选）**、**`.webp`** 或 **`.png`**，单图不超过 **500 KB**。
   - 命名建议与题号绑定，如 `assets/PHYS1001-exam-2024f-03-fig1.svg`。
   - 每张图必须在对应题目的 `stem.figures` / `answer.figures` / `solution.figures` / `options[].figures` 中声明（包含 `id`、`path`、`alt`），CI 会自动拦截未被引用的孤儿图片。
3. **如实标注答案来源 (`answer.origin`)**：
   - `official`：原卷参考答案、官方评分细则、教材书末参考答案
   - `community`：非官方书面详解、课程讲义或社区公开解答
   - `ai`：模型求解或贡献者独立推导
4. **稳定 ID 规范**：每道题的 `id` 必须以 `<course_code>-` 开头，仅包含 `[A-Za-z0-9._-]`，全局唯一且与内容位置绑定，禁止使用入库日期流水号。
5. **保留勘误记录**：若修正了原卷/原解本身的数学错误，请在 `quality.note` 简述原始错误与修正依据。
6. **合规与署名**：任何第三方来源必须在 `NOTICE.md` 中如实署名并标注对应 `source.rights`。

## 提交前本地校验

修改任意 `courses/*` 文件后，同步更新对应 `meta.json` 和根目录 `manifest.json` 中的统计与 SHA-256，然后运行：

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

两项全部通过后再提交 PR。
