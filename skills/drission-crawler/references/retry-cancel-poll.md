# timeout、poll、重试和取消

## 参数

每个流程显式声明 `timeout`、`poll`、`retry`、`max_depth`、`writeback`（含义见 SKILL.md）。`poll` 是条件轮询间隔，不是盲目延迟。

## 失败分类 → 处理

| 现象 / 异常 | 分类 | 处理 |
| --- | --- | --- |
| `ElementLostError`、`ContextLostError`、`PageDisconnectedError`、iframe 重建 | 作用域失效 | 重新 `get_frame` / `ele()` 后重试 |
| `ElementNotFoundError` / `NoneElement`，且页面仍在加载 | 短暂等待 | 保持当前步骤，按 `poll` 继续检查 |
| `ElementNotFoundError` / `NoneElement`，页面已稳定 | scope 或 locator 错 | 停止重试，记录候选证据，回到定位 |
| `CanNotClickError`、`is_covered=True` | 被遮挡 | `wait.not_covered` / 关闭遮罩后重试，不做 JS 强点 |
| `WaitTimeoutError` 但业务信号部分出现 | 就绪判定过严 | 按 ready-signals 分层重判，不加长盲等 |
| `TargetNotFoundError`、`BrowserConnectError` | 连接/tab 失效 | 重新 `get_tab(url=…)` 或重连 9222，见 live-browser-9222 |
| 业务字段明确为空 | 数据侧问题 | 进入记录回退或人工核验，不重复点击 |
| 保存 / 提交 / 发布等非幂等动作失败 | 非幂等 | 除非有明确幂等契约，不自动重复 |
| 用户取消 | 取消 | 在下一个可取消点原样传播 |

每次重试记录 `attempt`、原因、locator、scope 和后置条件；耗尽后输出最终证据，不静默吞错。

## 取消门禁

长轮询、记录循环、上传等待和重试之间都必须执行取消检查。单次 `ele()` 不能设成无法被取消的超长阻塞；用 `ele(loc, timeout=poll)` 短探测 + 外层 `deadline` 循环。
