---
name: work-doc-writer
description: >-
  Use when writing a program operation manual, technical specification, or
  delivery/case report as a Word file, including screenshot callouts.
  Triggers: 操作手册, 操作说明, 使用说明, 说明书, 技术文档, 成果报告, 案例材料,
  截图标注, user manual, spec docx. Do not use for 毕业论文 or theses
  (use word-thesis-format), slides, or marketing copy.
---

# 工作文档编写（操作手册 / 说明书 / 成果报告）

## 文档类型

| 类型 | profile | 何时用 | 骨架 |
|---|---|---|---|
| 操作手册 | `manual` | 给业务人员照着操作；默认类型 | [templates/manual.md](templates/manual.md) |
| 程序说明书 / 技术文档 | `spec` | 交付验收、存档，需要技术栈和流程图 | [templates/spec.md](templates/spec.md) |
| 成果报告 / 案例材料 | `report` | 评奖、汇报、案例申报 | [templates/report.md](templates/report.md) |

用户没说类型时，按"给谁看"判断：业务人员 → manual；验收存档 → spec；领导、评审 → report。拿不准就问。

## 开工前确认（缺哪项问哪项，一次只问一项）

1. 文档类型和标题（工具全称）。
2. 程序源码目录（manual / spec 必需）。
3. 截图文件夹（可选）。
4. 日期和版本号（默认今天、V1.0；改版时在版本表追加一行）。
5. 输出目录（默认放在源码目录的 `docs/` 下，没有源码目录就问）。
6. 是否同时要 PDF（默认只出 Word）。

## 流程

1. **读源码拿事实**：入口文件、GUI 文案（按钮、TAB、输入框标题、下拉选项、弹窗提示）、默认值、输入文件要求（文件名关键字、表头、目录结构）、输出文件和位置、需要人工介入的地方（登录、点"继续"）。整理成"功能清单 + 界面文案表"。源码里找不到的内容写"待确认"，不要编。
2. **截图对照（有截图时）**：按 [reference/screenshots.md](reference/screenshots.md) 逐张看图，写 `shots.json`，用 `annotate.py table` 输出对照表发给用户。**用户确认前不标注、不生成文档。**
3. **写源稿**：复制对应模板到输出目录，按 [reference/writing-style.md](reference/writing-style.md) 写成 `<文档名>.md`。源稿语法见 [reference/layout.md](reference/layout.md)。
4. **标注截图**：`annotate.py apply shots.json`，然后用 Read **逐张打开标注图**检查框的位置和序号。红框坐标必须按 [reference/screenshots.md](reference/screenshots.md) **第 6 节「红框像素校准」**取值与复核——禁止凭缩略图/视觉描述估坐标；不对就改坐标重画。
5. **检查源稿**：`check_doc.py`，ERROR 必须清零；WARN 逐条看，待确认项汇总给用户。
6. **生成并预览**：`build_docx.py --preview`，用 Read 打开预览页图检查（见"收尾验证"）。
7. **按需导出 PDF**：用户要时加 `--pdf`。

## 写作硬规则（详见 writing-style.md）

- 每个功能固定三段：准备数据 / 操作步骤 / 结果说明。网页录入、提交类程序用"资料准备：/ 生成配置：/ 开始录入：/ 人工核对："四标签变体。
- 步骤动词开头：准备、双击、选择、点击、填写、粘贴或拖拽、确认、核对、查看。一步一个动作。
- 按钮、TAB、输入框、文件名、文件夹名一律用中文引号，**名称和界面一字不差**。
- 功能描述"本工具用于……"；结果说明"系统会……"；可选项"如果选择……；不填写时系统会自动生成"；补充写进"（注：……）"。
- 涉及网页提交时写清边界：程序不自动提交或发布；完成录入不等于已保存或已提交。
- 不写实现原理和百科介绍；不用"您""温馨提示""恭喜"。
- 截图放在对应步骤之后，图题在图下方"图1-2 ××展示图"，图号按功能编号。

## 脚本

解释器：环境变量 `WORK_DOC_PYTHON` 有值时用它，否则用 PATH 上的 `python`。需要的包：python-docx、Pillow、PyMuPDF、PyYAML。本机可以先 `conda activate CreateReport`，或把该环境的解释器路径设进 `WORK_DOC_PYTHON`。下面 `<skill>` 指本 skill 目录。

```powershell
$PY = if ($env:WORK_DOC_PYTHON) { $env:WORK_DOC_PYTHON } else { "python" }
& $PY <skill>/scripts/annotate.py grid  <截图文件夹>          # 生成坐标网格副本，读框坐标用
& $PY <skill>/scripts/annotate.py table <shots.json>         # 输出对照表给用户确认
& $PY <skill>/scripts/annotate.py apply <shots.json>         # 画红框和序号
& $PY <skill>/scripts/check_doc.py <源稿.md> --code-dir <源码目录>
& $PY <skill>/scripts/build_docx.py <源稿.md> --preview <输出目录>/_preview [--pdf]
```

- `build_docx.py` 不加参数只生成 docx，目录是空域；加 `--finalize` / `--pdf` / `--preview` 时调用本机 Word（没有就用 WPS）刷新目录。
- `check_doc.py --code-dir` 会检查正文里加引号的界面名称是否在源码里出现，找不到的列为 WARN。
- 改了脚本先跑回归：`& $PY -m pytest <skill>/tests -q`。

## 收尾验证（按 dev-review-verify）

不能只看脚本退出码。必须：

1. 用 Read 打开 `_preview/page-*.png`：封面、目录有页码、标题编号连续、图片没被裁成一条、图题在图下方、表格没错位。
2. 用 Read 打开每张标注图（第 4 步已做则抽查）。
3. 回复用户时列出：docx（和 PDF）路径、预览看到的问题、待确认项清单、未做的验证。

## 不要做

- 不编造源码里没有的按钮、默认值、文件名。
- 不在用户确认对照表之前生成文档。
- 不擅自改用户给的单位模板；有模板时以模板为准（见 layout.md 第 4 节）。
- 不把截图里的账号、密码、身份证号原样放进文档，先提醒用户。

## 按需读取

| 文件 | 内容 |
|---|---|
| [reference/writing-style.md](reference/writing-style.md) | 固定句式、步骤动词、引号规则、安全边界、成果报告写法、错别字表、正反例 |
| [reference/layout.md](reference/layout.md) | 公文体版式参数、源稿语法、目录更新、已有模板时的处理 |
| [reference/screenshots.md](reference/screenshots.md) | 截图对照流程、shots.json、标注规范、复核清单、图题写法、**红框像素校准（第 6 节）** |
| [templates/](templates/) | 三类文档的源稿骨架 |
