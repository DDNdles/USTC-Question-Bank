# Contributing

欢迎提交题目勘误、补录新年份真题或贡献新课程题库。

## 基本规则

1. **严禁提交原始扫描件与二进制资产**：禁止提交 `.pdf`、`.png`、`.jpg`、`.sqlite`、`.zip` 或整本教材 OCR 原文。CI 会拦截此类文件。
2. **如实标注答案来源 (`answer.origin`)**：
   - `official`：原卷参考答案、官方评分细则、教材书末参考答案
   - `community`：非官方书面详解、课程讲义或社区公开解答
   - `ai`：模型求解或贡献者独立推导
3. **稳定 ID 规范**：每道题的 `id` 必须以 `<course_code>-` 开头，仅包含 `[A-Za-z0-9._-]`，全局唯一且与内容位置绑定，禁止使用入库日期流水号。
4. **保留勘误记录**：若修正了原卷/原解本身的数学错误，请在 `quality.note` 简述原始错误与修正依据。
5. **合规与署名**：任何第三方来源必须在 `NOTICE.md` 中如实署名并标注对应 `source.rights`。

## 提交前本地校验

修改任意 `courses/*` 文件后，同步更新对应 `meta.json` 和根目录 `manifest.json` 中的统计与 SHA-256，然后运行：

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

两项全部通过后再提交 PR。
