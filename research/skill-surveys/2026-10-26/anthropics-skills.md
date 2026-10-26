# Anthropic Skills（官方技能库）

查阅日：2026-10-26。

## 1. 来源

- 仓库：<https://github.com/anthropics/skills>
- 星标：183889（当日 GitHub API `stargazers_count`）
- 许可：仓库级 API 未给出 SPDX。README 写明其中许多技能为 Apache 2.0。抽查 `skills/skill-creator/LICENSE.txt`、`skills/internal-comms/LICENSE.txt`、`skills/frontend-design/LICENSE.txt` 均为 Apache 2.0。
- 文档技能另计：README 写明 `skills/docx`、`skills/pdf`、`skills/pptx`、`skills/xlsx` 为 source-available，不是开源。`docx` 的 frontmatter 标明专有条款，其 `LICENSE.txt` 为 Anthropic 保留权利，并指向 Anthropic 服务条款。本笔记不摘录这些目录中的步骤、脚本和提示。

## 2. 它是什么

这是 Anthropic 公布的 Agent Skills 示例库，不是单一技能。2026-10-26 的 `skills/` 下列有 19 个技能目录，覆盖文档、界面、品牌、内部沟通、网页测试、MCP，以及「怎样写技能」的 skill-creator。仓库还带 `spec/agent-skills-spec.md` 和 `template/`。

和本库最接近的公开部分有三类：skill-creator（如何写技能并做测试）、internal-comms（按文种路由到 `examples/`）、frontend-design（做界面时先定视觉方向）。docx 等文档技能展示了生产环境里「带脚本的技能」可以长到什么程度，但其许可不允许当作可复制实现。

## 3. 写法特点

- 每个技能一个目录，入口是 `SKILL.md`。公开样本的 frontmatter 至少有 `name`、`description`；internal-comms、frontend-design、docx 另有 `license` 字段，把许可放在技能入口，而不是只放在仓库根。
- description 写使用时机和触发词。docx 的 description 在写适用对象的同时，写明不用于 PDF、电子表格和与 Word 无关的一般编程。这是边界写在检索句里，而不是只写在正文后部。本笔记不转载该段原文。
- skill-creator 正文按「弄清意图、访谈与调研、写 SKILL.md、测试、再改」排列。写作指南的栏目包括技能解剖、渐进披露、避免意外、写法模式。测试要求同一轮里同时跑「带上该技能」和「不带该技能」的基线，再评分、看反馈、改技能。
- internal-comms 的 `SKILL.md` 很短：先判断文种，再打开 `examples/` 里对应的一份说明（3P 进展、公司简报、FAQ、其余沟通）。对不上已有文种就停下来问，不现场发明格式。
- frontend-design 把流程收成计划、对照任务说明检查、制作、自评，并要求视觉选择有依据，避免千篇一律的默认模板。
- 文档技能目录里是 `SKILL.md` 加 `scripts/`。README 把它们标成更复杂技能的参考。本笔记只确认目录和许可，不描述其操作方法。

## 4. 原理与设计意图

官方库要同时解决三件事：给标准一个可看的样子，给作者一条从起草到评测的路径，并把真正用于产品的文档能力以可阅读、不可随意复用的方式放出来。

渐进披露是为了控制上下文：入口只保留路由和硬规则，细则进 `examples/` 或 `references/`。description 写长，是因为宿主靠这段文字决定要不要加载技能。带技能与基线对照着跑，是为了证明「加了这段说明」确实改变结果，而不是只证明模型本来就会。

把专有文档技能和 Apache 技能放在同一仓库、用不同许可分开，是为了展示结构，同时挡住脚本和提示被直接拿走。

## 5. 对照本库

本库是招标、OCR、发票、比对归档、周报和 DEMO 开工一类交付 SOP。官方库里的 skill-creator、内部沟通和文档目录，是写法参考；不是第二套业务技能。

### 可借鉴

- `work-doc-writer` 已经按手册、说明书、成果报告分流到 `templates/`。internal-comms 说明这种「入口短、文种文件单列」可以再瘦一截：`SKILL.md` 只保留判断和停问，版式留在模板。
- `demo-kickoff-card`、`drission-crawler` 的 description 已写触发词和不用场景。可继续保持「不用」出现在 description 里，供宿主检索，而不只写在正文。
- skill-creator 的双轨测试可以补本库现有 `evals.json`。现有评测主要看该不该触发。对开工卡、工作文档，可以另加少量产物检查（四块是否齐全、按钮名是否回读自源码），与触发评测分开存放。
- 许可写进技能入口这一条，适合以后若有技能依赖上游限制时使用。`drission-crawler` 依赖的 DrissionPage 许可已写在仓库 README，不必把上游许可证全文贴进 `SKILL.md`。

### 不要照搬

- 不把 `docx`、`pdf`、`pptx`、`xlsx` 的脚本、提示或目录内容拷进 `work-doc-writer`、`word-thesis-format`。这两项继续用本库自己的模板和 `check_doc.py`、预览流程。
- 不把 frontend-design「要有辨识度、避开模板感」写进 `government-service-design`。政务后台要的是固定主色、表单表格和短文案，不是每页换一套视觉方向。
- 不把 skill-creator 整份评测器（并行试跑、查看器、基线对照）装进本库。本库没有那套运行器，触发样本保持在各技能 `evals/evals.json`。

## 6. 一句话建议

入口写清许可、触发和停用条件，细则放模板；专有文档技能只作结构对照，实现仍走本库自己的文档技能。
