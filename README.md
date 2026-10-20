# agent-skills

面向 Cursor 与 Codex 的 Agent Skills。  
来自真实交付，不是通用教程合集。

每个技能独立目录，入口为 `SKILL.md`。安装后，在对应工作场景中由 Agent 按需调用。

## 技能一览

| 技能 | 用途 |
| --- | --- |
| [`drission-crawler`](skills/drission-crawler/) | 浏览器自动化（DrissionPage）：等页面稳定、操作后核对结果。含广东招标投标监管网规则包。 |
| [`demo-kickoff-card`](skills/demo-kickoff-card/) | 开工前把业务口头交代整理成一张短说明，方便直接做 DEMO。信息不够处标「待确认」，不臆造。 |
| [`dev-process-handoff`](skills/dev-process-handoff/) | 功能、接口或验收标准有变时，写入项目交接文档。单测与实机验证分开写。 |
| [`government-service-design`](skills/government-service-design/) | 政务与企政后台界面：白底浅灰，主色 `#0A4CB5`，表单表格优先，文案从短。 |
| [`work-doc-writer`](skills/work-doc-writer/) | 写操作手册、说明书、成果报告。对照源码核对按钮文案；截图确认后再标注插入。公文体排版。 |
| [`word-thesis-format`](skills/word-thesis-format/) | 毕业论文 Word 排版：A4、小四宋体、1.5 倍行距、黑体标题。 |

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
