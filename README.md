# agent-skills

面向 Cursor 与 Codex 的 Agent Skills。  
来自真实交付，不是通用教程合集。

每个技能独立目录，入口为 `SKILL.md`。安装后，在对应工作场景中由 Agent 按需调用。

## 技能一览

| 技能 | 用途 |
| --- | --- |
| [`drission-crawler`](skills/drission-crawler/) | 用 DrissionPage 做稳定的浏览器自动化与网页采集：显式等待、定位、回读、重试与失败证据。已含广东省招标投标监管网（gd-zbtb）规则包。 |
| [`demo-kickoff-card`](skills/demo-kickoff-card/) | 编码前，把口头业务需求整理成 DEMO 开工卡（固定四块内容）。 |
| [`dev-process-handoff`](skills/dev-process-handoff/) | 功能行为、接口、默认值、页面流程或验收边界变化时，把关键点写入 CURRENT_HANDOFF 等交接文档。 |
| [`dev-review-verify`](skills/dev-review-verify/) | 收工验收：单测、sync 之后必须以 LIVE 收口。按项目配方卡直接跑，不向用户要测试数据；附交付包资源完整性检查脚本。 |
| [`windows-gui-bat-launcher`](skills/windows-gui-bat-launcher/) | Windows 交付包用 bat 启动桌面 GUI：黑框等待提示，窗口打开后写 ready 标志，bat 检测到后自动关闭。 |
| [`government-service-design`](skills/government-service-design/) | 政务 / 企业政务 GUI 设计规范：白底浅灰，默认主色 #0A4CB5；表单、表格、检索、状态与任务办理优先；文案短直。 |
| [`work-doc-writer`](skills/work-doc-writer/) | 编写程序操作手册、说明书/技术文档、成果报告 Word。先读源码取功能与界面文案；可按指定截图文件夹标注后插入。公文体版式。 |
| [`word-thesis-format`](skills/word-thesis-format/) | 编写或重排毕业论文 Word，应用论文版式（A4、25 mm 页边距、小四宋体 + Times New Roman、1.5 倍行距、黑体标题）。 |

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
- 项目配方卡：`dev-review-verify/references/projects/<代号>/`，只留本机、不入库（含本机路径）；入库的只有 `README.md` 与 `_template/`
- 本机建议用目录联接让 `~/.cursor/skills/<name>` 指向本仓库 `skills/<name>`，改一处即生效

## 免责

站点相关技能仅记录公开页面的定位与稳定性经验。默认不保存、不提交、不发布表单。使用须遵守目标站点条款与当地法律。
