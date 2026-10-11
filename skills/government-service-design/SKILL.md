---
version: alpha
name: government-service-design
description: >
  现代政务 / 企业政务类 GUI 设计规范。整体以白色与浅灰为基础，
  默认主色使用 #0A4CB5，强调正式、清晰、稳定、高效，不使用过度装饰、
  大面积渐变、夸张阴影或消费型视觉语言。界面以表单、表格、检索、
  状态反馈和任务办理为核心。GUI 中的标题、提示、说明、空状态和按钮文案
  必须精简，能用短语表达时不使用完整长句。

design_principles:
  default_color_rule: "当需求未明确指定主题色或主色时，统一使用 #0A4CB5。若已明确指定颜色，则优先遵循指定颜色。"
  style: "现代、正式、克制、清晰、可信、政务感"
  density: "中等偏紧凑，优先提高信息获取和业务办理效率"
  decoration: "少渐变、少阴影、少大圆角、少装饰性图形"
  hierarchy: "依靠字号、字重、间距、边框和浅色背景建立层级"
  copywriting: "GUI 文案短、直接、可扫描；避免冗长解释和重复提示"
  interaction: "操作结果明确，状态反馈简洁，不使用营销式或情绪化措辞"

colors:
  primary: "#0A4CB5"
  primary-hover: "#0C57CC"
  primary-active: "#083E94"
  primary-soft: "#EAF2FF"
  primary-disabled: "#B8CBE8"

  ink: "#1F2329"
  body: "#3B4654"
  muted: "#6B7280"
  muted-soft: "#9AA3AF"

  canvas: "#FFFFFF"
  surface-soft: "#F5F7FA"
  surface-muted: "#EEF2F7"
  surface-card: "#FFFFFF"

  border: "#D8DEE8"
  border-strong: "#B8C2CF"
  divider: "#E5EAF0"

  success: "#16865C"
  success-soft: "#E8F6F0"
  warning: "#C47A00"
  warning-soft: "#FFF5DF"
  error: "#C7352B"
  error-soft: "#FDEDEC"
  info: "#0A4CB5"
  info-soft: "#EAF2FF"

  on-primary: "#FFFFFF"
  on-dark: "#FFFFFF"
  scrim: "#000000"

color_rules:
  - "未指定主题色时，主按钮、主链接、选中态、焦点态、关键图标统一优先使用 {colors.primary}。"
  - "禁止为了丰富视觉而随意增加高饱和度辅助色。"
  - "语义色仅用于成功、警告、错误等明确状态，不替代主色。"
  - "大面积背景优先使用白色或浅灰，不使用大面积高饱和蓝。"
  - "图表未指定配色时，第一主序列使用 #0A4CB5，其余序列使用同色系明度变化或中性灰。"

typography:
  font-stack:
    fontFamily: "'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', 'Source Han Sans SC', Arial, sans-serif"

  display-lg:
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.35
    letterSpacing: 0

  display-md:
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0

  title-lg:
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0

  title-md:
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.45
    letterSpacing: 0

  title-sm:
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.45
    letterSpacing: 0

  body-md:
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0

  body-sm:
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0

  caption:
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0

  button-md:
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0

  nav-link:
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0

typography_rules:
  - "中文界面默认使用微软雅黑 / 苹方 / 思源黑体类无衬线字体。"
  - "不使用夸张超大标题；常规业务页面一级标题建议 20–24px。"
  - "正文以 14px 为主，辅助信息 12–13px。"
  - "不依赖超粗字重制造层级，正文 400，标题 500–600 即可。"
  - "同一页面字号层级不宜过多，通常控制在 4–5 档。"
  - "重要数据可适度放大，但避免金融大屏式视觉夸张。"

rounded:
  none: 0px
  xs: 2px
  sm: 4px
  md: 6px
  lg: 8px
  xl: 12px
  full: 9999px

rounded_rules:
  - "按钮、输入框默认 4px 圆角。"
  - "卡片、弹窗默认 6px 圆角。"
  - "大型容器不使用 16px、24px、32px 等消费型大圆角。"
  - "9999px 胶囊圆角仅用于状态标签、小型筛选标签，不用于主按钮和大面积搜索框。"

spacing:
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  base: 16px
  lg: 20px
  xl: 24px
  xxl: 32px
  section: 40px

layout:
  max_content_width: 1440px
  page_padding_desktop: 24px
  page_padding_tablet: 20px
  page_padding_mobile: 16px
  sidebar_width: 220px
  topbar_height: 56px
  form_label_width: "按业务需要设置，不强制固定"
  table_density: "中等偏紧凑"

layout_rules:
  - "桌面端优先充分利用横向空间，避免内容集中在页面中央形成大面积空白。"
  - "业务页面优先采用顶部导航 + 侧边导航 + 内容区结构。"
  - "查询条件较多时使用查询区 / 高级查询折叠，不把所有条件长期展开。"
  - "表格是主要数据承载方式，字段对齐、列宽、固定列和操作列优先考虑可读性。"
  - "表单分组使用分区标题、浅灰底或细分隔线，不依赖卡片堆叠。"

elevation:
  flat: "none"
  card: "0 1px 3px rgba(31, 35, 41, 0.08)"
  dropdown: "0 4px 12px rgba(31, 35, 41, 0.12)"
  modal: "0 8px 24px rgba(31, 35, 41, 0.16)"

elevation_rules:
  - "大多数页面保持平面化。"
  - "普通卡片可无阴影，仅使用 1px 边框。"
  - "阴影主要用于下拉菜单、浮层、弹窗等确有层级关系的组件。"
  - "禁止多层重阴影和悬浮式消费卡片效果。"

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
    height: 36px

  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"

  button-primary-active:
    backgroundColor: "{colors.primary-active}"
    textColor: "{colors.on-primary}"

  button-primary-disabled:
    backgroundColor: "{colors.primary-disabled}"
    textColor: "{colors.on-primary}"

  button-secondary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.primary}"
    borderColor: "{colors.primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.sm}"
    padding: "7px 15px"
    height: 36px

  button-default:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    borderColor: "{colors.border}"
    typography: "{typography.button-md}"
    rounded: "{rounded.sm}"
    padding: "7px 15px"
    height: 36px

  button-danger:
    backgroundColor: "{colors.error}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.sm}"
    height: 36px

  text-link:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"

  top-nav:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    height: 56px

  side-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    width: 220px
    borderColor: "{colors.divider}"

  side-nav-active:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    borderLeft: "3px solid {colors.primary}"

  page-header:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    padding: "16px 0"

  toolbar:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    padding: "8px 0"

  search-panel:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.body}"
    borderColor: "{colors.border}"
    rounded: "{rounded.md}"
    padding: "16px"

  content-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.body}"
    borderColor: "{colors.border}"
    rounded: "{rounded.md}"
    padding: "16px"

  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.border}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: "7px 10px"
    height: 36px

  text-input-focus:
    borderColor: "{colors.primary}"
    focusRing: "0 0 0 2px rgba(10, 76, 181, 0.12)"

  select:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.border}"
    rounded: "{rounded.sm}"
    height: 36px

  textarea:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    borderColor: "{colors.border}"
    rounded: "{rounded.sm}"
    padding: "8px 10px"

  table:
    headerBackground: "{colors.surface-muted}"
    headerTextColor: "{colors.ink}"
    bodyBackground: "{colors.canvas}"
    bodyTextColor: "{colors.body}"
    borderColor: "{colors.divider}"
    typography: "{typography.body-md}"
    rowHeight: "40px"

  table-row-hover:
    backgroundColor: "#F4F8FE"

  tabs:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    activeTextColor: "{colors.primary}"
    activeBorderColor: "{colors.primary}"

  pagination:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    activeBackground: "{colors.primary}"
    activeTextColor: "{colors.on-primary}"

  modal:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    rounded: "{rounded.md}"
    padding: "20px"

  drawer:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"

  status-tag:
    rounded: "{rounded.full}"
    typography: "{typography.caption}"
    padding: "2px 8px"

  alert-info:
    backgroundColor: "{colors.info-soft}"
    textColor: "{colors.body}"
    borderColor: "{colors.primary}"

  alert-success:
    backgroundColor: "{colors.success-soft}"
    textColor: "{colors.success}"

  alert-warning:
    backgroundColor: "{colors.warning-soft}"
    textColor: "{colors.warning}"

  alert-error:
    backgroundColor: "{colors.error-soft}"
    textColor: "{colors.error}"

  empty-state:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"

  footer:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.muted}"
    borderColor: "{colors.divider}"

---

# Overview

这是面向政务系统、事业单位内部系统、公共服务平台和企业政务类后台的现代 GUI 设计规范。

整体视觉以 **白色 + 浅灰 + 政务蓝** 为核心。默认主色为 **#0A4CB5**。若需求中没有明确指定颜色，所有主按钮、选中态、焦点态、主链接、关键操作图标和主要图表序列优先使用该颜色；若需求已指定颜色，则遵循明确指定值。

设计目标不是“传统老旧政务网页”，也不是“互联网消费产品”，而是：

- 正式，但不沉重。
- 现代，但不过度装饰。
- 信息密度较高，但不拥挤。
- 操作明确，减少理解成本。
- 表格、表单、查询、审批、状态、材料和流程优先。
- GUI 文字尽可能短，不写大段提示。

# Core Style

## 1. 政务感

政务感主要通过以下方式建立，而不是依靠大面积深蓝：

- 稳定的蓝白灰配色。
- 清晰的标题层级。
- 规则化表格和表单。
- 4–6px 小圆角。
- 细边框和浅灰分区。
- 克制的阴影。
- 明确、直接的操作语言。
- 统一的状态反馈。

禁止为了“显得高级”大量使用玻璃拟态、霓虹渐变、发光边框、超大圆角、悬浮卡片和复杂装饰背景。

## 2. 默认颜色规则

**硬规则：当没有指定主题色时，使用 `#0A4CB5`。**

适用于：

- 主按钮
- 当前菜单
- 当前 Tab
- 选中状态
- 焦点边框
- 主链接
- 关键图标
- 进度条主色
- 单序列图表
- 主要强调数字

不适用于：

- 成功：使用绿色
- 警告：使用橙色
- 错误 / 删除：使用红色
- 禁用：使用灰色或低饱和蓝灰

不要因为已有主色蓝，就把所有文字、边框、图标都变蓝。

# GUI 文案规则

GUI 中的提示文字必须精简。

## 基本原则

1. 能用 2–6 个字说明，就不要写完整长句。
2. 按钮使用“动作词”，不要写解释句。
3. 字段附近已有标题时，不重复标题内容。
4. 普通常识操作不增加无意义说明。
5. 一个区域尽量只保留一条关键提示。
6. 错误提示直接说明问题和处理方式。
7. 成功反馈只说明结果，不写庆祝式文案。
8. 不使用营销式、情绪化、拟人化语言。
9. 不连续堆叠多个“温馨提示”“友情提示”“特别说明”。
10. 必须说明复杂规则时，优先使用“查看规则”“说明”折叠展开。

## 推荐

- `请输入项目名称`
- `请选择日期`
- `保存成功`
- `上传失败，请重试`
- `暂无数据`
- `未查询到结果`
- `确认删除？`
- `最多上传 10 个文件`
- `仅支持 PDF、DOCX`
- `数据已更新`
- `处理中…`

## 避免

- `请您在此处输入需要查询的项目名称信息`
- `恭喜您，您的数据已经成功保存完成`
- `温馨提示：请认真检查您所填写的所有内容是否准确无误`
- `当前暂时没有可以向您展示的数据内容`
- `您是否确认要执行删除当前这条数据的操作？`

## 按钮文案

优先：

- 查询
- 重置
- 新增
- 保存
- 提交
- 导入
- 导出
- 下载
- 上传
- 编辑
- 删除
- 返回
- 关闭
- 确认
- 取消
- 查看
- 办理
- 审核
- 通过
- 退回

避免：

- 点击查询
- 立即开始查询
- 保存当前信息
- 确认并继续下一步
- 点击这里查看更多

除非业务确有歧义，否则按钮通常控制在 **2–4 个汉字**。

# Typography

中文默认优先使用：

`Microsoft YaHei` → `PingFang SC` → `Noto Sans CJK SC` → `Source Han Sans SC` → system sans-serif

建议层级：

| 场景 | 字号 | 字重 |
|---|---:|---:|
| 页面主标题 | 20–24px | 600 |
| 区块标题 | 16–18px | 600 |
| 表单 / 表格正文 | 14px | 400 |
| 辅助信息 | 12–13px | 400 |
| 按钮 | 14px | 500 |

原则：

- 避免 32px 以上的大标题占据业务页面。
- 正文统一优先 14px。
- 不要每个区域都加标题。
- 已通过布局能够理解的信息，不再增加说明文字。
- 数字型核心指标可适当放大，但保持克制。

# Layout

## 页面结构

桌面端推荐：

`顶部栏 + 左侧导航 + 主内容区`

典型主内容区：

1. 面包屑 / 页面标题
2. 查询条件
3. 操作工具栏
4. 表格 / 表单 / 业务内容
5. 分页或操作区

不要把每一块内容都套成独立大卡片。

## 查询区

- 简单查询：单行排列。
- 条件较多：两到四列栅格。
- 非核心条件：放入“更多条件”。
- 查询按钮放在条件末端或右侧。
- 默认按钮：`查询`
- 辅助按钮：`重置`

不要为查询区域增加大段操作说明。

## 表单

- 标签简短。
- 必填使用 `*` 或统一必填标识。
- 帮助文字仅在确有规则时出现。
- 错误信息紧邻字段显示。
- 长表单按业务分组，不按视觉效果过度拆卡。
- 同一组控件高度保持一致，默认 36px。

## 表格

政务 / 后台系统优先保证表格可读性。

- 表头使用浅灰背景。
- 表头字重 500–600。
- 行高约 40px。
- 关键字段允许固定列。
- 操作列放在右侧。
- 数值右对齐。
- 状态居中或按业务统一。
- 超长文本省略并支持悬浮查看或详情查看。
- 不使用明显斑马纹，必要时仅使用极浅隔行色。
- Hover 只做轻微浅蓝背景。

# Components

## Button

主按钮：

- 背景：`#0A4CB5`
- 文字：白色
- 高度：36px
- 圆角：4px
- 字号：14px
- 字重：500

次按钮：

- 白底
- 蓝色文字或深灰文字
- 1px 边框
- 4px 圆角

同一区域通常只保留一个主按钮，避免多个高强调按钮同时出现。

## Input / Select

- 高度：36px
- 圆角：4px
- 默认边框：`#D8DEE8`
- Focus：`#0A4CB5`
- Placeholder：灰色
- 不使用厚重内阴影
- 不使用胶囊输入框

## Card

- 白底
- 1px 浅灰边框
- 6px 圆角
- 内边距 16px
- 默认无阴影或仅极轻阴影

能通过分隔线和背景分区解决时，不增加卡片层级。

## Tabs

- 默认文字：深灰
- 当前项：`#0A4CB5`
- 当前项使用底部 2px 蓝色线
- 不使用大面积胶囊 Tab，除非是小型筛选器

## Modal

- 圆角：6px
- 标题：16–18px / 600
- 正文：14px
- 底部按钮靠右
- 主要动作使用 `#0A4CB5`
- 提示尽量一句话完成

示例：

`确认删除该记录？`

而不是：

`请确认您是否真的需要删除当前所选择的这条记录，删除后可能无法恢复。`

若不可恢复确实重要，可写：

`删除后不可恢复，确认删除？`

## Status

状态标签用于快速扫描，不写长句。

推荐：

- 待提交
- 待审核
- 审核中
- 已通过
- 已退回
- 已完成
- 已作废
- 已关闭

标签可使用轻背景 + 深色文字，不使用高饱和实心色大面积填充。

## Empty State

默认：

`暂无数据`

查询无结果：

`未查询到结果`

不要使用：

`这里空空如也`
`暂时还没有任何内容哦`

# Icons

- 使用线性、简洁、统一风格图标。
- 常规尺寸 16px / 18px / 20px。
- 主操作图标可使用 `#0A4CB5`。
- 普通工具图标使用深灰。
- 不依赖彩色图标表达层级。
- 不使用卡通、手绘、拟物图标。
- 图标旁已有文字时，不额外增加解释。

# Feedback

## Success

优先：

`保存成功`
`提交成功`
`导入完成`

## Error

优先：

`保存失败，请重试`
`文件格式不支持`
`网络异常，请重试`

错误信息要说明问题，但不要一次展示技术堆栈或大段后台异常。

## Loading

优先：

`加载中…`
`处理中…`
`正在导入…`

不要使用连续变化的长句。

# Responsive Behavior

| 设备 | 建议 |
|---|---|
| Mobile | 单列布局，表格按业务改为列表或横向滚动，主要操作固定在易触达区域 |
| Tablet | 查询区 2 列，表格保留主要字段 |
| Desktop | 查询区 2–4 列，完整表格与侧边导航 |
| Wide | 内容区可扩展，但避免无限拉宽正文和表单 |

桌面政务系统优先保证 1366px、1440px、1920px 宽度下均可正常使用。

# Accessibility

- 正文和背景保证足够对比度。
- 不只依靠颜色表达成功、错误和选中状态。
- 输入框必须有明确 Focus 状态。
- 按钮禁用状态应可区分。
- 表单错误应有文字说明。
- 点击目标建议不小于 32px，高频操作优先 36–40px。
- 键盘操作场景下保留清晰焦点。

# Design Output Rules

当生成 GUI、网页、HTA、桌面工具、管理后台或业务系统界面时：

1. 未指定颜色：主色使用 `#0A4CB5`。
2. 已指定颜色：遵循用户指定颜色，不强制覆盖。
3. 默认使用现代政务风格，不使用 Airbnb、Apple 营销页式大留白和消费型大圆角。
4. GUI 提示文字必须精简。
5. 无必要不增加副标题、说明段落、帮助文字。
6. 无必要不增加装饰性卡片。
7. 主界面优先突出业务内容和操作，而不是品牌视觉。
8. 数据型页面优先表格、筛选、状态和操作效率。
9. 默认圆角 4–6px。
10. 默认阴影轻或无阴影。
11. 主按钮默认使用 `#0A4CB5`。
12. 页面背景优先 `#FFFFFF` / `#F5F7FA`。
13. 图标、边框和辅助文字使用中性灰，避免全页面蓝色化。
14. 弹窗和提示内容优先 1–2 行完成。
15. 删除、作废、退回等高风险操作必须有明确确认，但确认文案仍保持简短。

# Quick Reference

```text
默认主色      #0A4CB5
页面背景      #FFFFFF
浅灰背景      #F5F7FA
表头背景      #EEF2F7
主文字        #1F2329
正文          #3B4654
辅助文字      #6B7280
边框          #D8DEE8

按钮高度      36px
输入框高度    36px
按钮圆角      4px
输入框圆角    4px
卡片圆角      6px
弹窗圆角      6px

页面标题      20–24px / 600
区块标题      16–18px / 600
正文          14px / 400
辅助文字      12–13px / 400

关键词：
正式 / 现代 / 克制 / 清晰 / 稳定 / 高效 / 蓝白灰 / 少圆角 / 少阴影 / 短文案
```
