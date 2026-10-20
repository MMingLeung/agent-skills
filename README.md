# agent-skills

面向 Cursor 与 Codex 的 Agent Skills。  
来自真实交付，不是通用教程合集。

每个技能独立目录，入口为 `SKILL.md`。安装后，在对应工作场景中由 Agent 按需调用。

## 技能一览

| 技能 | 用途 | 边界 |
| --- | --- | --- |
| [`drission-crawler`](skills/drission-crawler/) | DrissionPage 浏览器自动化：显式等待、操作回读、失败可追。含广东招标投标监管网站点包。 | 不替代 Playwright / Selenium；不编造 locator 清单 |
| [`demo-kickoff-card`](skills/demo-kickoff-card/) | 将口头业务需求压成四格「DEMO 开工卡」。缺项标注「待确认」。 | 非完整需求规格书 |
| [`dev-process-handoff`](skills/dev-process-handoff/) | 行为、接口、默认值或验收口径变更时，写入交接文档。 | 静态检查与单测不得表述为 live |
| [`government-service-design`](skills/government-service-design/) | 政务 / 企政后台 GUI：白底浅灰，主色 `#0A4CB5`，表单与表格优先，文案从短。 | 不用于营销落地页 |
| [`work-doc-writer`](skills/work-doc-writer/) | 操作手册、程序说明书、成果报告。自源码提取界面文案；截图经对照确认后标注并入文。公文体版式。 | 不用于毕业论文 |
| [`word-thesis-format`](skills/word-thesis-format/) | 毕业论文 Word 版式（A4、小四宋体、1.5 倍行距、黑体标题）。 | 工作文档见 `work-doc-writer` |

## 安装

**Cursor**

```bash
cp -R skills/<name> ~/.cursor/skills/<name>
```

**Windows (PowerShell)**

```powershell
Copy-Item -Recurse skills\<name> $HOME\.cursor\skills\<name>
```

**Codex**：目标目录改为 `~/.codex/skills/`。

安装后建议新开对话。将 `<name>` 替换为上表技能目录名。

## 维护约定

- 通用规则：技能根目录与 `references/`
- 站点专用选择器与 SOP：`references/sites/<代号>/`
- 不提交：`output/`、真实截图、`.env`、Cookie
- 新站点：按 `templates/site-pack-template.md` 建包，并更新本页索引

## 免责

站点相关技能仅记录公开页面的定位与稳定性经验。默认不保存、不提交、不发布表单。使用须遵守目标站点条款与当地法律。
