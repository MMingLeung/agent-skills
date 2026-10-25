---
name: drission-crawler
description: >-
  Use when driving a real browser with DrissionPage and the run must wait,
  locate in scope, read back, and retry. Triggers: DrissionPage, tab.ele,
  get_frame, 9222, CDP, iframe, Vue/React 动态页, 点了没反应, 串数据,
  gd-zbtb. Do not use for Playwright or Selenium code, plain requests or HTML
  parsing, a locator-only dump, or a flow JSON/YAML runner.
---

# DrissionPage 稳定执行

🌐 用 DrissionPage 操作真实浏览器时读这份说明：每一步先等页面就绪，再定位、操作，然后读回结果；失败就留下证据，再重试或停下来。

## 适用与不适用

适用：任何用 DrissionPage（`Chromium` / `ChromiumOptions` / `tab` / `frame`）操作真实浏览器的任务，包括新起浏览器与 9222 接管。

不用本技能：

- Playwright / Selenium 代码 → 只可借用本技能的协议思想，不套用 API 与 SOP；
- 纯 `requests` / HTML 解析，无浏览器；
- 只打开页面抓一份元素清单：不适用本技能的步骤协议与站点包；
- 不操作浏览器、只把业务编成 flow JSON/YAML 交给别的运行器：不适用。

## 硬性步骤协议

每个页面动作都按此顺序完成，未通过当前后置条件不得进入下一步：

```text
明确 scope（tab / frame / modal / form）
→ 显式等待元素或业务状态（timeout + poll）
→ 定位并记录候选证据
→ 执行动作（原生优先）
→ 判断业务后置条件
→ 回读关键值/状态
→ 分类失败
→ 按 retry + poll 重试、回退或中止
→ 通过后进入下一步
```

每个任务须能追溯到以下参数（含义见下表，模板见 [templates/step-template.json](templates/step-template.json)）：

| 参数 | 含义 | 默认建议 |
| --- | --- | --- |
| `timeout` | 单个等待条件的上限（秒） | 15～30 |
| `poll` | 条件轮询间隔（秒），不是盲等 | 0.3～0.5 |
| `retry` | 同一步骤最大尝试次数 | 3 |
| `max_depth` | 允许下钻的 iframe / 弹窗层数，超出即视为 scope 错误 | 1～2 |
| `writeback` | 结果落到哪里：`log` / `file` / `db` / `none` | `log` |

禁止：

- 用固定 `sleep` 代替业务后置条件；
- 只找到元素就认为点击或输入成功；
- 输入后不重新定位回读 `value`；
- 重绘、切页、切 iframe、新 TAB 后复用旧 `tab` / `frame` / `ele`；
- 未证明作用域就遍历全部 frame 或全页搜索；
- 失败后无条件重复点击或提交；
- 把单元测试、CONFIG 加载或静态检查写成 live 成功；
- 用「页签激活」「全局 loading 壳」「列表/侧栏首项稳定」单独充当「可截图/可入库」就绪；截图、入库、回读字段必须等到层 3（业务区）就绪（分层判定见 [ready-signals.md](references/ready-signals.md)）。

## 开工检查清单

1. 记录 `tab.url`、`tab.title`、`tab.tab_id`，确认在哪个 `frame`。
2. 用 `tab.wait.ele_displayed` / `ele.wait.displayed` + `poll` 等进入条件。
3. 选 locator：id/name → 容器内语义 CSS → CSS+精确文本 → 有 live 证据才用 XPath/位置。
4. 记录候选数量、`states.is_displayed`、`is_enabled`、文本、class、`html[:200]`。
5. 操作前重新 `ele()` 取最新元素。
6. 用业务信号验证后置条件，并回读关键字段。
7. 失败按 [retry-cancel-poll.md](references/retry-cancel-poll.md) 分类；用户取消原样传播。
8. 保存失败证据；默认不保存、不提交、不发布任何表单。

## 读文件路由

只读与当前任务匹配的文件，一次只进一层：

| 任务类型 | 读 |
| --- | --- |
| 任何点击/输入/导航 | [step-contract.md](references/step-contract.md)、[drissionpage-adapter.md](references/drissionpage-adapter.md)、[retry-cancel-poll.md](references/retry-cancel-poll.md) |
| 新站摸索 / 录制不稳 / 截到空壳 / SPA 填了不搜 | 再加 [probe-stabilize.md](references/probe-stabilize.md)（跨站「探针→稳态」方法） |
| iframe、Vue/React 表单、动态列表、重绘 | 再加 [iframe-vue-react.md](references/iframe-vue-react.md) |
| 多 TAB / 侧栏卡片 / 右侧表单 / loading 判定 / 多条记录循环 | 再加 [ready-signals.md](references/ready-signals.md) |
| 接管已开浏览器（9222）、CONFIG 结束后二次连接 | [live-browser-9222.md](references/live-browser-9222.md) |
| 写失败日志、DOM 快照、截图 | [failure-evidence.md](references/failure-evidence.md) |
| 具体站点 | 通用规则之后再读 `references/sites/<站点>/`，见 [sites/README.md](references/sites/README.md) |

### 站点包索引

命中任一「触发线索」就在通用规则之后读对应站点包；站点包与通用规则冲突时，以站点包的 live 证据为准。

| 代号 | 站点 | 触发线索（URL / iframe / 业务词） | 入口 |
| --- | --- | --- | --- |
| `gd-zbtb` | 广东省招标投标监管网 | 监管网、`gdzbtb`、`iframe[name=trading-info]`、`platform-detail`、节点发布情况、项目台账登记、招标项目信息、中标候选人、合同公示、`gmd-spin` | [locator.md](references/sites/gd-zbtb/locator.md) → 症状速查与 SOP-A～K 见 [sop-detail-tab-refresh.md](references/sites/gd-zbtb/sop-detail-tab-refresh.md) |

新站点按 [templates/site-pack-template.md](templates/site-pack-template.md) 建包，并在此表和 [sites/README.md](references/sites/README.md) 各加一行；站点选择器、UI 库 class、业务 TAB 名不要写回通用文件。

#### gd-zbtb 症状 → SOP 速查

命中 `gd-zbtb` 时，遇到下列症状先按对应 SOP 处理，而不是加长盲等（SOP 正文在 [sop-detail-tab-refresh.md](references/sites/gd-zbtb/sop-detail-tab-refresh.md)）：

| 症状 | SOP |
| --- | --- |
| TAB 已点亮但采到上一 TAB 卡片 / 节点串名 | SOP-C（内容关键字 + 标题集合，日期可相同） |
| `get_frame(trading-info)` / CDP `li.item` 超时 | SOP-A + SOP-D（重取 frame、收窄列表 locator） |
| 登录 CONFIG 成功后采集立刻失败 | SOP-F（settle、按 URL 选 tab、列表/详情判别） |
| 固定 TAB 枚举报「未找到」 | SOP-B（只采实际存在的 TAB） |
| GUI 长时间无日志 | SOP-F（stdout/stderr 接日志队列 + 进度文案） |
| 右侧已渲染仍报「loading」空等 | SOP-H + SOP-K（表单优先；`nested-loading` 壳 ≠ 真 loading） |
| 截图空白 / 表单未刷出就截图 | SOP-H（右侧业务表单/只读区可见后再截；入口落地 ≠ 表单就绪）；通用方法见 [probe-stabilize.md](references/probe-stabilize.md) |
| 第 2 个项目搜索框空、列表未过滤 | SOP-I（每轮写框/点查询前重取 `trading-info` iframe） |
| 详情入口侧栏长期「…招标文件」导致落地超时 | SOP-H（入口只等 TAB + 侧栏稳定；业务字段以目标 TAB 右侧表单为准） |
| 只需台账登记表却在遍历全部 TAB | SOP-J（列表 √× + 仅合同 TAB） |

SOP-A～K 一览：A iframe 重取 · B 只采实际 TAB · C 切 TAB 内容信号 · D 侧栏 locator · E 列表 vs 详情 · F handoff 二次连接 · G 9222 验收 · H 三层就绪 · I 每轮重取 iframe · J 台账轻量采集 · K 假 loading。

## 高频失败速查（通用）

| 症状 | 先查 |
| --- | --- |
| 新站不知点哪 / 录制回放就挂 / 截到空壳 | 先探针对比空态vs就绪，再语义步骤 → [probe-stabilize.md](references/probe-stabilize.md) |
| 点了没反应 / 点了但状态没变 | 是否在旧 frame；`states.is_clickable`/`is_covered`；后置条件是否用业务信号 → adapter、ready-signals |
| `ElementNotFoundError` / 返回 `NoneElement` | scope 错、iframe 未取、页面重绘 → adapter「作用域」 |
| `ElementLostError` / `ContextLostError` | 节点已重建，重新 `ele()`/`get_frame()` 再试 → retry-cancel-poll |
| 输入后回读为空或被回填 | Vue/React 模型未更新 → iframe-vue-react |
| 切 TAB/记录后采到上一条数据 | 只等了激活态，没等内容信号 → ready-signals |
| 已渲染仍报 loading 空等 | loading 容器壳 ≠ 真转圈 → ready-signals「假 loading」 |
| 第 N 轮搜索框空 / 列表未过滤 | 复用上一轮 frame → ready-signals「每轮重取」 |
| 点击后新窗口找不到 | 用 `browser.wait.new_tab` 或 `ele.click.for_new_tab` 并按 URL 选 tab → adapter「多 TAB」 |
| 9222 刚连上就报错 | 与上一连接竞态、选错 tab → live-browser-9222 |
| 批量里某条被「已完成，跳过」 | 检查点主键撞车（如只按代码，同码多行）→ 下节「人在环批处理」 |
| 用户点「继续」后整批报错停 | 继续后的回读用了硬校验 → 下节「人在环批处理」 |

## 排障先读落盘日志

用户报「报错 / 跳过 / 卡住」时，**先自己读**最新一批的运行日志、进度、报告（如 `*.run.jsonl`、`*.progress.json`、`*.run-report.json`、`执行记录.log`），按时间对上用户说的那一步，再看代码。不要先让用户贴日志；读不到再问。

## 人在环批处理（暂停 → 用户处理 → 点继续）

逐条录入、中间弹窗让人补录或保存的批处理，统一按这三条：

1. **检查点主键按业务行唯一**：用「业务编号 + 名称 + 序号」这类组合，不要只用一个可能重复的编号（同一投资代码下施工 / 监理是两条）。合并组才用组键。
2. **用户点「继续」后的回读默认软校验**：字段为空、元素找不到 → 记 `warnings`，带进下一个人工弹窗，继续流程；**不整批终止**。只有「继续会写错数据」的安全前置条件才硬停（如当前页不是空白新增页、作用域不对）。
3. **跳过、警告都写进报告**：进度文件里每条要能看出是已完成、跳过还是带警告完成，以及原因。

## 验证边界

- 未连接真实浏览器时不得声称 live 验证通过。
- 9222 验证从当前失败步骤继续，保留现场，不关闭、不重启用户浏览器。
- 单元测试、CONFIG 加载、live readback、真实保存必须分别报告。
- 修改 locator、可见性或 iframe 范围策略前，必须先取得现场日志和快照证据。
- 汇报用 [templates/live-probe-report.md](templates/live-probe-report.md)。
