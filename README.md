# agent-skills

交付现场留下的技能。  
给 Cursor / Codex。

每个目录一份 `SKILL.md`。

---

### drission-crawler
等待。回读。可插拔站点包。  
含广东招标投标监管网。

### demo-kickoff-card
口头需求 → 四格开工卡。  
缺项标「待确认」。

### dev-process-handoff
行为与验收变更，写入交接。  
单测不作 live。

### government-service-design
政务 GUI。白、灰、`#0A4CB5`。  
短文案。少装饰。

### work-doc-writer
操作手册 / 说明书 / 成果报告。  
源码取文案。截图经确认后入文。

### word-thesis-format
毕业论文版式。仅此。  
工作文档见 `work-doc-writer`。

---

## 安装

```bash
cp -R skills/<name> ~/.cursor/skills/<name>
```

```powershell
Copy-Item -Recurse skills\<name> $HOME\.cursor\skills\<name>
```

Codex：`~/.codex/skills/`。

---

站点包只记公开页的定位经验。默认不保存、不提交、不发布。
