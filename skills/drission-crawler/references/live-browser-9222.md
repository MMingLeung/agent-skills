# 接管已开浏览器（9222）与 live 验证

## 连接

```python
from DrissionPage import Chromium, ChromiumOptions
co = ChromiumOptions().set_local_port(9222)   # 或 Chromium('127.0.0.1:9222')
browser = Chromium(co)
tab = browser.get_tab(url='目标站点关键字')    # 不要盲信 latest_tab
```

开始前记录：`tab.url`、`tab.title`、`tab.tab_id`、debug port。然后分别探测 root 与每个 frame：候选数、可见文本、`html[:200]`、frame path。每次只推进一个业务动作，记录动作前后状态和回读值。

## 上一连接刚结束后的二次连接

前一个进程（GUI / CONFIG 引擎）刚对同一浏览器收尾时再 `Chromium(9222)`：

1. 短 settle（1～2 秒 poll 检查 `browser.tab_ids`），避免与刚收尾的 CDP 竞态；
2. 按 URL 选目标 tab；
3. `get_frame` 失败要 poll + 多 locator，勿把瞬时 `ElementNotFoundError` 当终态；
4. 区分列表与详情后再决定是否导航（见 [ready-signals.md](ready-signals.md)「列表 vs 详情」）。

## 安全边界

- 默认停在保存前；不保存、不提交、不发布。
- 不 `browser.quit()`、不 `close_tabs()` 用户的页面，不重启浏览器。
- 失败后保留现场，供下一步继续。
- 没有真实 DOM / readback 时，只能报告静态或测试证据。

## 证据分层

汇报必须区分：

1. 单元测试；
2. CONFIG / schema 加载；
3. live locator / readback；
4. 真实保存 / 提交验证。

模板：[templates/live-probe-report.md](../templates/live-probe-report.md)。
