# agent-skills

本仓库收录本人在企业办公自动化与采购档案智能化落地过程中沉淀的一组 Agent Skills（智能体技能说明）。技能面向 Cursor、Claude Code 等环境：装入对应目录后，助手可按约定完成需求整理、界面与文档编写、浏览器操作步骤编排及 Windows 启动脚本等交付环节，并在收工时对照真实产物完成核对，为同类任务的规范交付提供支撑。

## 📦 安装

建议按需安装单个技能。将下方 `<name>` 替换为技能目录名（如 `work-doc-writer`）。

**Cursor（用户级，本机各项目可用）**

```bash
cp -R skills/<name> ~/.cursor/skills/<name>
```

安装后请新开对话再提需求。说明见 [Cursor Agent Skills](https://cursor.com/docs/skills) 与 [Claude Code skills](https://code.claude.com/docs/en/skills)。

<details>
<summary>Windows、Claude Code、Codex，或仅当前仓库使用</summary>

**Claude Code（用户级；仅当前仓库则拷贝至 `.claude/skills/<name>`）**

```bash
cp -R skills/<name> ~/.claude/skills/<name>
```

**Windows PowerShell（Cursor 用户级）**

```powershell
Copy-Item -Recurse skills\<name> $HOME\.cursor\skills\<name>
```

**仅当前 Cursor 仓库**：拷贝至项目内 `.cursor/skills/<name>`。

**Codex**：目标目录改为 `~/.codex/skills/`。

</details>

## 🧭 适用场景

按日常工作场景选用；单次任务通常对应其中一至两个技能。

| 场景 | 技能 | 常用说法 |
| --- | --- | --- |
| 动手开发前先把口头需求整理清楚 | [`demo-kickoff-card`](skills/demo-kickoff-card/) | 「先整理成一页，暂不写代码。」 |
| 按步骤操作浏览器页面并回读结果 | [`drission-crawler`](skills/drission-crawler/) | 「用浏览器把列表抓下来。」 |
| 提供 Windows 双击启动方式 | [`windows-gui-bat-launcher`](skills/windows-gui-bat-launcher/) | 「双击后等待窗口就绪再退出提示框。」 |
| 政务或企业内部后台界面规范 | [`government-service-design`](skills/government-service-design/) | 「后台按政务风格，表单与表格优先。」 |
| 依据源码编写操作手册、技术说明或成果报告 | [`work-doc-writer`](skills/work-doc-writer/) | 「起草操作手册。」 |
| 毕业论文 Word 版式规范 | [`word-thesis-format`](skills/word-thesis-format/) | 「按学校格式排版。」 |
| 收工前对照真实产物核对 | [`dev-review-verify`](skills/dev-review-verify/) | 「打开实际结果再核对。」 |
| 行为或验收标准变更后留存交接说明 | [`dev-process-handoff`](skills/dev-process-handoff/) | 「更新交接说明，不以聊天记录为准。」 |

## 📋 技能说明

| 技能 | 作用 |
| --- | --- |
| [`demo-kickoff-card`](skills/demo-kickoff-card/) | 需求整理卡：动手开发前，将口头需求整理为「背景、输入输出、决策与禁止事项、成功标准」四块内容的一页清单。 |
| [`drission-crawler`](skills/drission-crawler/) | 基于 DrissionPage 编排真实浏览器操作：等待页面稳定、定位与点击、回读结果；失败时保留证据。含广东省招标投标监管网（gd-zbtb）规则包。 |
| [`windows-gui-bat-launcher`](skills/windows-gui-bat-launcher/) | Windows 下以 bat 启动桌面程序：提示等待，窗口就绪后自动关闭提示框。 |
| [`government-service-design`](skills/government-service-design/) | 政务及企业内部后台界面约定：白底浅灰、表单表格与查询办理优先、文案简短。未指定颜色时主按钮默认 `#0A4CB5`。 |
| [`work-doc-writer`](skills/work-doc-writer/) | 对照程序源码编写操作手册、技术说明或成果报告（Word），截图可加标注。 |
| [`word-thesis-format`](skills/word-thesis-format/) | 按固定版式规范毕业论文 Word（如 A4、页边距 25 mm、正文小四宋体等）。 |
| [`dev-review-verify`](skills/dev-review-verify/) | 收工核对：在真实环境打开本次产物再验收；单测通过不能代替实机核对。 |
| [`dev-process-handoff`](skills/dev-process-handoff/) | 交接说明：行为、接口、默认值或验收标准变更时，写入变更摘要、依据文档与完成标准。 |

## 🗺️ 推荐使用路径

多数交付任务按下列顺序推进：先整理需求，再按场景选用实现类技能，随后在真实环境核对，行为有变更则更新交接说明。

```mermaid
flowchart LR
  kickoff["demo-kickoff-card<br/>需求整理"] --> build["按场景选用实现技能"]
  build --> review["dev-review-verify<br/>真实环境核对"]
  review --> handoff["dev-process-handoff<br/>交接说明"]
```

实现类技能包括：`drission-crawler`、`windows-gui-bat-launcher`、`government-service-design`、`work-doc-writer`、`word-thesis-format`。

以「公告发布时间导出」为例：先整理需求整理卡并确认四块内容；再按卡实施（浏览器采集走 `drission-crawler`）；按 `dev-review-verify` 打开页面与导出文件核对两行；最后按 `dev-process-handoff` 写入交接说明。

## ❓ 说明

**是否需要一次安装全部技能？**  
不必。按当前任务安装所需技能即可，避免无关说明干扰对话。

**安装后未见变化？**  
请新开对话后再提需求，或明确指定技能目录名。

**仓库中为何没有 `INDEX.md`？**  
`dev-review-verify` 下的 `references/projects/INDEX.md` 为本机验收备忘（含本机路径与命令），不纳入公开仓库。技能将改看当前仓库的 `AGENTS.md`、`CURRENT_HANDOFF` 及 `scripts/*live*` 等文件。

**是否会自动改动正式系统？**  
需求整理卡中应写明禁止事项。浏览器采集默认不保存、不提交、不发布网页表单。使用时须遵守目标网站条款及当地法律。

**与 DrissionPage 的关系**  
仅 `drission-crawler` 使用 [DrissionPage](https://github.com/g1879/DrissionPage)。上游许可对商业使用有限制，以 [LICENSE](https://github.com/g1879/DrissionPage/blob/master/LICENSE) 为准。

## 🔧 维护约定

本仓库技能自真实交付中抽取。修改时请注意：

- 通用规则置于技能根目录 `SKILL.md` 与 `references/`；站点专用选择器与步骤置于 `references/sites/<代号>/`
- 不提交 `output/`、真实截图、`.env`、Cookie
- 新站点按 [`templates/site-pack-template.md`](skills/drission-crawler/templates/site-pack-template.md) 建包，并更新本页技能表
- 项目级验收备忘仅保留在本机；入库仅含 [`README.md`](skills/dev-review-verify/references/projects/README.md) 与 [`_template/`](skills/dev-review-verify/references/projects/_template/)
- 各技能含 `evals/evals.json`（约 3 条应触发、2 条不应触发），供回归核对

## ⚠️ 许可与注意事项

`drission-crawler` 依赖上游 DrissionPage。个人可用于学习及合法非盈利用途；未经版权持有人授权，不得将源码或二进制用于商业行为。详情以官方 LICENSE 为准。

与具体网站相关的技能，仅记录公开页面的定位与等待方式；默认不保存、不提交、不发布表单。
