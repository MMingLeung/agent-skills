---
name: dev-process-handoff
description: >-
  Use when a change alters behavior, an API, a default, a page flow, or
  acceptance criteria and that fact must land in a handoff document.
  Triggers: handoff, CURRENT_HANDOFF, 交接文档, 验收口径, 开发过程关键点.
  Do not use for formatting-only refactors or tests that do not change
  what "done" means.
---

# 开发过程关键点交付物（Handoff）

📌 功能、接口、默认值、页面流程或验收标准有变化时，把「这次改了什么、以何为准、怎么验收」写进交接文档，不要只留在聊天里。

## 何时必须用

任务导致下列任一变化时，**同一任务内**更新交付物后再结束：

- 功能行为 / 业务规则
- 接口、字段、CONFIG、默认值
- 页面流程、locator、TAB、作用域
- 验收边界、门禁、禁止事项

**不强制**仅为了「有文档」而改文档：

- 纯格式化、不改行为的重构
- 单纯补测试且不改验收口径

## 任务开始：发现并读取

1. 若仓库有 `AGENTS.md` / `.cursor/rules`，先读其中对 handoff / 专题文档的路由。
2. 按项目约定定位交付物根；常见路径（存在则用，勿臆造）：
   - `docs/**/CURRENT_HANDOFF.md`
   - `docs/CURRENT_HANDOFF.md`
   - `CURRENT_HANDOFF.md`
3. 若有索引（如 `docs/**/00_index.md`）：先读索引 → `CURRENT_HANDOFF.md` → 索引路由到的受影响专题。
4. **专题/handoff 与源码不一致时**：以当前源码、定向测试、约定的 live 回读为准；回写文档消除偏差。

没有既有 handoff 时：在任务收尾提出最小落地路径（默认 `docs/CURRENT_HANDOFF.md`），征得同意后再创建；不要在无关仓库里批量铺文档树。

## 任务结束：写什么

更新 `CURRENT_HANDOFF.md`（及受影响专题），只记可交接事实：

| 必写 | 说明 |
|------|------|
| 变更摘要 | 行为/接口/默认值/流程改了什么 |
| 单一事实来源 | 以哪份专题或代码为准 |
| 验收口径 | 怎样算过；门禁与禁止项 |
| 验证类型 | 静态检查 / 单测 / 定向脚本 / **LIVE** 须分开写；LIVE 是收工最后一道验收（见 `dev-review-verify`） |
| 未做事项 | 明确未验证、未 LIVE、未提交、未发布的部分；缺 LIVE 不得写成已验收通过 |

模板见 [templates.md](templates.md)。

## 硬性禁止（跨项目）

- 不得把**静态源码检查**或**单元测试 / pytest**写成 live / 实页 / 联调成功。
- 不得把「读过文档」写成「已在目标环境验证」。
- 不得把 sync / 归类探针 / 交付物源码字符串检查写成 LIVE 已通过。
- 收工顺序以 `dev-review-verify` 为准：**最后必须 LIVE**；未 LIVE → handoff/回复只能写「未验收完成」。
- 默认不保存、不提交、不发布网页表单或生产配置（除非用户明确要求）。
- 只编辑本任务授权文件；不覆盖、回退、删除或带入无关改动。

## 与仓库本地规则的关系

- **全局 Skill**：规定「要不要写、写什么、验证怎么表述」。
- **仓库 `AGENTS.md` / rules**：规定「读哪几份路径、专题目录名、环境解释器」等项目特例。
- 两者冲突时：项目路径与业务禁令以仓库为准；「不得伪造成功验证」以本 Skill 为准且不可放宽。

## 收尾检查

```text
- [ ] 若行为/接口/默认值/流程/验收有变 → 已更新 CURRENT_HANDOFF（及专题）
- [ ] 验证表述未把静态/单测写成 live
- [ ] 若本任务改了运行时行为：已做 LIVE，或已标明「未验收完成」+ 阻塞原因
- [ ] 未擅自保存/提交/发布表单或生产配置
- [ ] 无既有 handoff 时已确认路径或已跳过（纯格式/纯测试）
```
