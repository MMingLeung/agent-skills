# 交付包路径布局（跨项目通用）

改交付 bat / sync / 子包内调试工具，或用户问「打包了产物怎么还在子目录 / 找不到入口」时读本节。  
**本机绝对路径、某仓库 sync 命令表**仍写在 `references/projects/<代号>/delivery.md`（本机专用，不入库）。

## 两层根目录

| 根 | 含义 | 典型内容 |
| --- | --- | --- |
| **交付根** | 用户双击 bat、放运行时、看日志的目录 | `【总入口】.bat`、各 `启动*.bat`、`py11/`、`chrome/`、`output/`、`config/` |
| **子包根** | sync 进去的功能代码目录 | `tool_hub/`、`archive_auto_entry/`、`pdf_*`、`announcement_*` 等 |

## 硬性约定

1. **用户可见产物默认写交付根**  
   日志、`.ready_*`、探针/跑批报告、台账（若未另指定）→ `交付根/output/…`。  
   不要默认写到 `子包根/output/`，除非该子包明确要求包内隔离。

2. **bat 与业务代码路径必须一致**  
   bat 通常 `cd /d "%~dp0"`，日志写 `%~dp0output\`（交付根）。  
   业务里用 `Path(__file__).parents[N]` 时：若落在子包名（如 `archive_auto_entry`），产物基路径应为 `package_root.parent / "output" / …`，与 bat 对齐。

3. **开发仓入口 ≠ 交付入口名**  
   开发仓可用 `scripts/_tmp_*.py`；交付内常去掉 `_tmp_` 或改名，并用交付根 bat 启动。  
   sync 若跳过 `_tmp_*`，必须**显式注入**交付入口文件，并在校验里断言存在。

4. **库模块无 `__main__` 不能当启动器**  
   只 `python xxx_lib.py` 会 exit 0 无输出；交付/文档只宣传 bat 或带 `main` 的入口脚本。

5. **注入源要写清**  
   若交付子包来自旁路仓库，但调试工具以另一仓为准：sync 须写明「从哪拷、覆盖谁」，避免「只改了旁路源、交付仍是旧注入」。

## py11 附属 exe（可选精简）

- **可删**：`site-packages` 内工具型 `.exe`（如 PyInstaller bootloader、protoc.exe、pythonwin.exe、setuptools cli/gui、pip distlib、pythonservice.exe）。一般不影响 GUI 的 import 运行时。
- **禁止删**：交付根 `py11/python.exe`、`py11/pythonw.exe`。
- **勿因「带 exe」整包删** 推理大包（如 `torch/`）——OCR 等链可能依赖。

## 验收（路径类改动）

1. sync 后：交付根有 bat；子包内有对应 py。  
2. LIVE：在**交付根**跑 bat/入口，确认报告/日志落在交付根 `output\`。  
3. 禁止把「只在开发仓跑通」写成「交付路径已正确」。

## 与项目包分工

| 内容 | 放哪 |
| --- | --- |
| 上述通用规则 | 本文件（入库、可推 GitHub） |
| `<诗颖>` 绝对路径、具体 sync 脚本名、ZIP 名单、某功能注入文件表 | `references/projects/<代号>/delivery.md`（本机，gitignore） |
