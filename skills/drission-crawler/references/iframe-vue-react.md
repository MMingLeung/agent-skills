# iframe、Vue/React 与动态列表

## 切换 iframe

```text
确认外层页面状态
→ 等待目标 iframe 出现/loaded
→ frame = tab.get_frame(loc)
→ 在 frame 上重新获取根容器和关键元素
```

- 不能因为 URL 或 hash 没变就认为页面完成切换。
- 父页面 `tab.ele` 通常找不到 iframe 内业务控件；DrissionPage 免的是 `switch_to.frame`，不是「不用取 frame」。
- 切页、导航、iframe 重建后必须重新 `get_frame`，见 [drissionpage-adapter.md](drissionpage-adapter.md)「作用域」。
- `max_depth` 之内才允许继续下钻嵌套 iframe；超出说明 scope 判断有误，先回到证据。

## Vue/React 输入

统一执行：重新定位 → `input(clear=True)` → 重新定位 → 回读 `value` → 失败留证。

- 原生输入被模型回填、节点重建或回读为空时，才使用 `input(by_js=True)` 或 `run_js` setter，且必须派发 `input`、`change`、`blur` 后再回读。
- 下拉/级联/日期组件：以「选中标签文本或内部值回读正确」为后置条件，不以「弹层关闭」为准。

## 动态记录切换

```text
保存切换前 payload 签名（数量 + 首项标题）
→ 点击目标记录
→ 回读目标标题/status/active
→ 重新 get_frame / 取 scope
→ 等待旧 payload 消失或新 payload 出现
→ 等待关键字段数量/值满足条件
→ 才读取表格
```

- 不能把相同的名称、表头或非空输入框当作刷新完成条件。
- 缺少关键字段时使用有界短探测并进入下一条，不能对每行字段使用长 `timeout` 逐项阻塞。

## 多 TAB 详情 / 侧栏卡片 / 右侧表单 / loading

页签 `active` ≠ 侧栏已刷新 ≠ 右侧表单已渲染。分层就绪、内容信号、假 loading、每轮重取作用域的判定方法见 [ready-signals.md](ready-signals.md)。截图类动作必须在层 3 就绪后执行。
