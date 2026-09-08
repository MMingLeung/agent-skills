# 页面步骤契约

每个步骤都必须有可观察的输入、动作、后置条件和失败证据。推荐使用以下结构描述 CONFIG 或实现代码：

```json
{
  "step_id": "fill_project_name",
  "scope": "frame: css:iframe[name='main']",
  "wait": {
    "locator": "css:input[name='projectName']",
    "state": "visible",
    "timeout": 30,
    "poll": 0.5
  },
  "locate": {
    "locator": "css:input[name='projectName']",
    "visible_only": true,
    "expected_count": 1
  },
  "action": {
    "type": "input",
    "clear": true,
    "value": "..."
  },
  "postcondition": {
    "type": "readback",
    "locator": "css:input[name='projectName']",
    "expected_value": "..."
  },
  "retry": {
    "max_attempts": 3,
    "retryable_errors": ["ElementLostError", "ContextLostError", "iframe_rebuilt"]
  },
  "max_depth": 1,
  "writeback": "log",
  "cancel_check": true,
  "evidence_on_failure": true
}
```

空模板见 [templates/step-template.json](../templates/step-template.json)。

## 后置条件示例

| 动作 | 可接受的后置条件 |
| --- | --- |
| 点击 tab | `active` 改变且目标容器出现业务内容（见 ready-signals） |
| 点击打开新窗口 | `browser.wait.new_tab` 命中且新 tab URL 非 about:blank |
| 输入文本 | 重新定位后 `value` 等于期望值 |
| 选择下拉项 | 选中标签/内部值回读正确 |
| 点击查询 | 结果列表、准确 toast 或明确错误出现 |
| 点击保存 | 返回列表或出现明确业务结果 |
| 上传文件 | 当前弹窗可见预期文件名且 loading 消失 |
| 切换动态记录 | 标题/status/active 正确，旧 payload 不再残留 |

同一个输入框“仍然非空”不能证明动态记录已经刷新；必须有记录特有的 payload、signature、候选数量或其他业务信号。
