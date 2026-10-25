---
name: windows-gui-bat-launcher
description: >-
  Use when a Windows delivery package starts a PyQt or desktop GUI from a .bat
  and the console should show a wait message, then close after the window is up.
  Triggers: 启动黑框, ready 标志, 双击闪退, python.exe, bat launcher,
  startup wait, PermissionError 日志抢锁. Do not use for web apps, services,
  or a silent pythonw-only launcher.
---

# Windows GUI 交付启动（bat 等待 ready）

跨项目通用：双击 bat → 黑框提示等待 → GUI 就绪 → 黑框自动关。

## 何时必须用

- 写/改交付物 `.bat` 启动 PyQt6 / 桌面 GUI
- 用户提到：黑框、python、启动等待、ready、双击闪退、bat 打不开
- 他机交付「只要双击就能开」

## 标准流程（默认）

1. **bat 可见**：显示「正在启动…请稍候…」（不要用纯隐藏 VBS/mshta 作为默认）。
2. **后台启进程**：只用 `py11\python.exe`（**不要用 pythonw**——失败无控制台痕迹，难排障）。  
   用 `start /B "" "%PYTHON%" ... >>"%LOG%" 2>&1`，错误进 bat 日志。
3. **GUI 就绪信号**：窗口 `show` + `processEvents` 后写  
   `output/.ready_<name>`（UTF-8 文本即可）。
4. **bat 轮询**：检测到 ready 文件 → 提示「程序已打开」→ 短延时 → `exit` 关黑框。
5. **超时**：到点仍无 ready → `type` 日志并 `pause`（不要静默失败）。
6. **日志分离**：bat 写 `output/startup_bat_*.log`；程序写 `output/app_*.log`，**禁止**与 bat 抢同一文件（避免 Windows `PermissionError`）。

## 硬性验证（LIVE）

与 `dev-review-verify` 一致：**LIVE 是收工最后一道验收**；单测/静态检查不能代替。

改 bat / `mark_gui_ready` / 交付入口后，**同一任务内必须 LIVE 实跑**：

1. 删除旧 `output/.ready_*`（若有）。
2. 用 `cmd /c` 实际执行交付根对应 `.bat`（或等价：同环境 `python -m <module>`）。
3. 在超时前确认：
   - 进程未立刻退出；
   - `output/.ready_<name>` 已生成；
   - GUI 窗口已出现（或日志出现 `shown` + ready 文件）。
4. 再结束窗口 / 杀进程。

**禁止**把「读过 bat / sync 成功 / 静态 import」写成启动已验证。  
未做 LIVE 时，handoff 必须写明「启动未 LIVE」。

## Python 侧（必写）

```python
def mark_gui_ready(name: str) -> Path:
    path = app_root() / "output" / f".ready_{name}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("ready\n", encoding="utf-8")  # 源码里写 \\n 转义，勿把真换行嵌进引号
    return path

# window.show() / raise_ / activateWindow() 之后：
app.processEvents()
mark_gui_ready("tool_hub")  # 与 bat 中 READY 名一致
```

生成交付 `paths.py` 时：模板里用 `"ready\\n"`，**不要**再 `.replace(...)` 成真实换行（会弄断字符串 → `SyntaxError`，pythonw 下完全静默）。

## bat 模板

可复制模板：[templates/gui-ready-launcher.bat](templates/gui-ready-launcher.bat)。

把 `tool_hub`、`your_package`、日志名改成当前工具。模板里已经包含：可见的「正在启动」提示、`py11\python.exe`（不用 pythonw）、ready 轮询、超时 `type` 日志并 `pause`、bat 日志与程序日志分开。

## 排障

| 现象 | 排查 |
|------|------|
| 黑框等到超时 | 未 `mark_gui_ready`；READY 名不一致；`paths.py` SyntaxError；看 bat 日志 traceback |
| 用 pythonw 无窗口无日志 | **改回 python.exe + 重定向日志**；勿再用 pythonw 作默认 |
| `SyntaxError: unterminated string` in paths | 生成脚本把 `"ready\n"` 写成了真换行 |
| `PermissionError` 写日志 | bat/程序抢同一 log |
| 找不到 python | 缺 `py11\python.exe` |

## 明确不做（除非用户点名）

- 默认不用 `pythonw.exe`
- 默认不提供独立 `.vbs` 启动器
- 默认不把「完全无黑框」当第一方案
- 不写死某机 conda 路径（交付只用相对 `py11`）

## 与仓库约定

项目若有 `AGENTS.md` / 交付 sync：bat 与 `mark_gui_ready` 由 sync 生成；改完必须 LIVE 跑 bat，再更新 handoff。
