# DrissionPage 适配规则（4.x）

## 对象层级

```text
Chromium(addr_or_opts)          浏览器
  .latest_tab / .get_tab(url=…) / .get_tabs() / .new_tab() / .activate_tab()
  .wait.new_tab(timeout)
tab                             页签
  .get(url) .ele() .eles() .get_frame() .get_frames()
  .wait.ele_displayed() .wait.doc_loaded() .wait.url_change() .wait.title_change()
  .run_js() .get_screenshot() .listen
frame = tab.get_frame(loc)      iframe 文档作用域，API 与 tab 基本一致
ele                             元素
  .click() .click.for_new_tab() .input(vals, clear=) .clear() .value .attr() .text .html
  .states.is_displayed / is_enabled / is_clickable / is_covered / is_alive
  .wait.displayed() .wait.clickable() .wait.not_covered()
```

默认 `Settings.raise_when_ele_not_found = False`：`ele()` 找不到返回 `NoneElement`（布尔为 False），**不会抛错**。任何 `ele()` 结果都要先判真，不要把 `NoneElement` 当成功。

## 定位顺序

1. 稳定 `#id` / `[name=…]`。
2. 当前容器内的语义 CSS（`css:div.panel input[placeholder*=…]`）。
3. CSS 候选 + 精确文本过滤（`tab.ele('css:.tab-item', ...)` 后比对 `text`，或 `@@text()=`）。
4. 只有 live 证据时才用 XPath、`nth-of-type`、位置序号。

禁止默认：绝对 XPath、全页重复文本、跨全部 frame 搜索、全页 `li.item` 这类宽泛列表选择器。

## 作用域

- 每次动作前确认在 `tab` 还是某个 `frame`，以及是否在 modal/form 内。
- DrissionPage 免的是 Selenium 式 `switch_to.frame`，**不是**「父页面直接点 iframe 内元素」。父页面 `tab.ele` 通常找不到 iframe 内控件，必须 `frame = tab.get_frame(loc)` 后在 `frame` 上操作。
- 切 TAB、导航、重绘、iframe 重建、循环进入下一条记录后，**重新 `get_frame`**，禁止复用旧 `frame` / `ele`。
- `get_frame` 失败：捕获 `ElementNotFoundError` / 超时 → 按 `poll` 重试；多 locator 回退（`css:iframe[name=…]`、`xpath://iframe[@src*=…]`、`get_frames()` 按 name/url 识别）；耗尽后抛可读 `RuntimeError`（带 `tab.url`）。
- 列表类元素必须收窄到容器内：`frame.ele('css:div.wrapper ul.list').eles('css:> li')`，禁止在整页高频 `eles('css:li.item')`。

## 等待

- 进入条件：`tab.wait.ele_displayed(loc, timeout=…)`、`ele.wait.displayed()`、`ele.wait.clickable()`。
- 页面导航：`tab.wait.load_start()` → `tab.wait.doc_loaded()`；URL/标题变化用 `wait.url_change` / `wait.title_change`。
- 业务状态：把 `ele()` + `states` 放在 `while time.time() < deadline` 的 poll 循环里，条件是**业务信号**，不是「元素存在」。
- 单次 `ele(loc, timeout=poll)` 用短超时，外层循环负责总 `timeout` 与取消检查。

## 原生动作优先

- 默认 `ele.click()`、`ele.input(vals, clear=True)`。
- `click()` 不抛异常 ≠ 成功；必须验证业务状态。`Settings.raise_when_click_failed` 可开，但只当作证据。
- 输入后必须 `ele = scope.ele(loc)` 重新定位再读 `ele.value`。
- 只有 live 证据证明原生动作不触发框架模型时，才用 `input(by_js=True)` / `run_js` setter，并派发 `input`、`change`、`blur` 后回读。

## 多 TAB

```text
before = set(browser.tab_ids)
ele.click()                                # 或 new_tab = ele.click.for_new_tab(timeout=…)
new_tab = browser.wait.new_tab(timeout=…)  # 返回 tab_id 或 tab（按版本）
new_tab = browser.get_tab(url=…)           # 有多候选时按 URL 选，不盲信 latest_tab
poll 直到 new_tab.url 非 about:blank 且 doc_loaded
```

- 新 TAB 出现后，旧 `tab` 仍可用，但业务动作要在**目标** tab 上做。
- 关闭 tab 前确认不是用户手工打开的页面。

## 候选证据

每次更换 locator 前记录：scope/frame path、候选数量、`is_displayed`、`is_enabled`、`is_covered`、文本、class、`html[:200]`、异常类型。
