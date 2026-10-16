# Design Tokens

本文件存放完整设计 token，供实现 GUI / 写 CSS 变量时按需读取。主决策规则见 [SKILL.md](SKILL.md)。

```yaml
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
```

