---
name: drission-crawler
description: "用 DrissionPage 稳定执行浏览器自动化与网页采集：显式等待、作用域定位、后置条件、回读、retry+poll、失败证据。适用于 Chromium/Chromium(9222) 接管、iframe、Vue/React 动态页、多 TAB、动态列表、假 loading。用户提到 DrissionPage、tab.ele、get_frame、9222/CDP 接管、动态页采集不稳、点了没反应、串数据时使用；内含按站点拆分的兼容规则包（已有：广东省招标投标监管网 gd-zbtb）。不用于 Playwright/Selenium 代码、纯 requests 解析、抓 locator 清单或编写 flow JSON。"
---

# DrissionPage 稳定执行

## 适用与不适用

适用：任何用 DrissionPage（`Chromium` / `ChromiumOptions` / `tab` / `frame`）操作真实浏览器的任务，包括新起浏览器与 9222 接管。

不用本技能：

- Playwright / Selenium 代码 → 只可借用本技能的协议思想，不套用 API 与 SOP；
- 纯 `requests` / HTML 解析，无浏览器；
- 只要打开页面抓元素清单 → `drissionpage-element-capture`；
- 要把业务编成 flow JSON/YAML 跑框架 → `web-automation-product-framework`。

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
- 用「页签激活」「全局 loading 壳」「列表首项稳定」单独充当「可截图/可入库」就绪（见 [ready-signals.md](references/ready-signals.md)）。

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

## 高频失败速查（通用）

| 症状 | 先查 |
| --- | --- |
| 点了没反应 / 点了但状态没变 | 是否在旧 frame；`states.is_clickable`/`is_covered`；后置条件是否用业务信号 → adapter、ready-signals |
| `ElementNotFoundError` / 返回 `NoneElement` | scope 错、iframe 未取、页面重绘 → adapter「作用域」 |
| `ElementLostError` / `ContextLostError` | 节点已重建，重新 `ele()`/`get_frame()` 再试 → retry-cancel-poll |
| 输入后回读为空或被回填 | Vue/React 模型未更新 → iframe-vue-react |
| 切 TAB/记录后采到上一条数据 | 只等了激活态，没等内容信号 → ready-signals |
| 已渲染仍报 loading 空等 | loading 容器壳 ≠ 真转圈 → ready-signals「假 loading」 |
| 第 N 轮搜索框空 / 列表未过滤 | 复用上一轮 frame → ready-signals「每轮重取」 |
| 点击后新窗口找不到 | 用 `browser.wait.new_tab` 或 `ele.click.for_new_tab` 并按 URL 选 tab → adapter「多 TAB」 |
| 9222 刚连上就报错 | 与上一连接竞态、选错 tab → live-browser-9222 |

## 验证边界

- 未连接真实浏览器时不得声称 live 验证通过。
- 9222 验证从当前失败步骤继续，保留现场，不关闭、不重启用户浏览器。
- 单元测试、CONFIG 加载、live readback、真实保存必须分别报告。
- 修改 locator、可见性或 iframe 范围策略前，必须先取得现场日志和快照证据。
- 汇报用 [templates/live-probe-report.md](templates/live-probe-report.md)。
