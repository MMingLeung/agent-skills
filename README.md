# agent-skills

交付里反复用的 Cursor / Codex 技能。

不是通用教程合集，是我从招标监管录入、操作手册、政务 GUI、论文排版里抠出来的写法——agent 读了能少问、少编、少假验证。

每个目录一个技能，入口是 `SKILL.md`。装到本机后，在对话里提到对应场景就会（或应）被用上。

## 先装哪个

按你现在在干的事选，不必全装：

| 你在干嘛 | 装这个 | 一句话 |
| --- | --- | --- |
| 浏览器自动录入、动态页老点不中 | [`drission-crawler`](skills/drission-crawler/) | 稳定等待 + 回读；广东监管网有现成站点包 |
| 口头需求要开工 DEMO | [`demo-kickoff-card`](skills/demo-kickoff-card/) | 压成四块短卡，缺的标「待确认」 |
| 行为 / 接口 / 验收变了要留交接 | [`dev-process-handoff`](skills/dev-process-handoff/) | 写进 CURRENT_HANDOFF；单测别冒充 live |
| 政务后台蓝白灰界面 | [`government-service-design`](skills/government-service-design/) | 默认主色 #0A4CB5，短文案，少装饰 |
| 操作手册 / 说明书 / 成果报告 | [`work-doc-writer`](skills/work-doc-writer/) | 公文体；截图先出对照表再画红框 |
| 自考 / 毕业论文 Word | [`word-thesis-format`](skills/word-thesis-format/) | 只管论文版式；工作文档用上面那个 |

写 `work-doc-writer` 之前，交付手册按钮名常和界面不一致，截图红框也对不齐步骤。现在约定：先读源码拿文案，截图先给你确认对照表，再生成 Word。

## 安装（Cursor）

把某个技能目录拷进个人 skills 目录，例如：

```bash
cp -R skills/work-doc-writer ~/.cursor/skills/work-doc-writer
```

Codex 同理，目标改成 `~/.codex/skills/`。装完新开一轮对话更稳。

Windows 可用资源管理器复制，或 PowerShell：

```powershell
Copy-Item -Recurse skills\work-doc-writer $HOME\.cursor\skills\work-doc-writer
```

## 我怎么维护这些技能

- 通用规则放技能根目录和 `references/`
- 某个网站的选择器、SOP 放 `references/sites/<代号>/`
- 不提交 `output/`、真实截图、`.env`、Cookie
- 新站点按 `templates/site-pack-template.md` 建包，并改索引

## 免责

站点相关技能只记公开页上的定位与稳定性经验，默认不保存、不提交、不发布表单。使用请遵守目标站点条款和当地法律。
