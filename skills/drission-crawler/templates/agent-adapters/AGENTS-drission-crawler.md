## DrissionPage 稳定执行技能

任务用 DrissionPage 操作真实浏览器（新起 Chromium 或 9222 接管、iframe、Vue/React 动态页、多 TAB、动态列表）时，必须先读取并遵循：

`~/.cursor/skills/drission-crawler/SKILL.md`（Codex 为 `~/.codex/skills/drission-crawler/SKILL.md`）

每一步必须：明确 scope → 显式等待 → 定位留证 → 操作 → 业务后置条件 → 回读 → 按 `retry + poll` 处理失败，确认成功后才进入下一步。默认不保存、提交或发布网页表单。站点专用选择器放 `references/sites/<站点>/`。
