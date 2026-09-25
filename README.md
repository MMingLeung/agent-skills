# agent-skills

工作中沉淀的 Agent Skills 公开库。每个技能一个目录，入口为 `SKILL.md`。

## 安装

### Cursor

```bash
cp -R skills/drission-crawler ~/.cursor/skills/drission-crawler
```

### Codex

```bash
cp -R skills/drission-crawler ~/.codex/skills/drission-crawler
```

## 已收录

| 技能 | 说明 |
| --- | --- |
| [`drission-crawler`](skills/drission-crawler/) | DrissionPage 稳定执行协议 + 可插拔站点兼容包（含广东省招标投标监管网 `gd-zbtb`，SOP-A～K） |
| [`demo-kickoff-card`](skills/demo-kickoff-card/) | 口头业务需求（3～8 条要点）压成四块短「DEMO 开工卡」，缺字段标 `待确认`，DEMO 默认只读/本机 |
| [`dev-process-handoff`](skills/dev-process-handoff/) | 行为 / 接口 / 默认值 / 流程 / 验收口径变化时，把开发过程关键点写入 `CURRENT_HANDOFF` 与受影响专题；静态检查、单测、live 回读分开表述 |

## 贡献约定

- 通用协议放在技能根目录与 `references/*.md`
- 站点专用选择器与 SOP 放在 `references/sites/<代号>/`
- 不要提交 `output/`、截图、`.env`、账号 Cookie 等证据文件
- 新站点按 `templates/site-pack-template.md` 建包，并更新站点索引表

## 免责声明

站点包仅记录公开页面上的定位与稳定性经验，默认不保存、不提交、不发布表单。使用时请遵守目标站点服务条款与当地法律法规。
