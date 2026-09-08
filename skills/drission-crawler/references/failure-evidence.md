# 失败证据

失败记录至少包含：

```text
timestamp
step_id/name
URL/title/tab_id
frame_path/scope
locator
candidate_count
visible/enabled
action
postcondition
attempt/retry/poll/timeout
error_type/message
HTML or DOM snapshot reference
screenshot reference when visual state matters
```

日志不输出账号、密码、Token、Cookie、Authorization、手机号、邮箱等敏感明文。异常应保留 traceback，并按项目要求脱敏。
