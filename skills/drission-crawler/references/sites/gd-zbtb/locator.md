# 站点包 gd-zbtb：广东省招标投标监管网 locator

监管网任务必须先证明当前浏览器 scope，再修改 locator 或 CONFIG。通用方法见 `references/*.md`，本文只记站点选择器。

## 必做 live probe

1. 保持调试浏览器打开，不关闭、不重启。
2. 记录当前 tab URL/title。
3. 分别探测外层 root 与 `iframe[name="trading-info"]`：候选数量、可见文本、HTML/class/text。
4. 只根据现场证据决定 iframe 或 locator 变化。

## 常见作用域

| 元素 | 作用域 |
| --- | --- |
| 外层“新建招标项目” | root |
| 交易类型/业务类别弹窗 | `trading-info` iframe |
| 能源电力树节点 | `trading-info` iframe |
| 公开招标/邀请招标 | `trading-info` iframe |
| 公告表单输入 | `trading-info` iframe |
| 发布信息列表 / 详情 TAB / 侧栏卡片 | `trading-info` iframe |

## 发布信息列表 ↔ 详情（节点发布类采集）

| 步骤 | Locator / 规则 |
| --- | --- |
| iframe | `iframe[name=trading-info]`（失败则 `get_frames` 按 name/url 回退） |
| 列表搜索 | `input[placeholder*='招标项目名称']` + 列表行 / `span.tendering` |
| 进详情 | 行内**第一个** `span.tendering-status-green`（不要用数字文本）；台账轻量采集可**优先点合同列绿格** |
| 详情 TAB | `.tab-list .my-gmd-bu_content`；激活态 `div.active-list.tab-list …` |
| 侧栏卡片 | `div.wrapper ul.list > li.item`（禁止全页 `li.item`） |
| 合同 TAB 右侧就绪 | `el-form-item` + label 含「合同名称/合同金额/…」；**勿**用 `gmd-spin-nested-loading` 当 loading（见 SOP-K） |
| 台账截图 | 列表窗口图在点绿格**前**；合同窗口图在 SOP-H 层 3 就绪**后** |

列表/详情易混：详情也可能有搜索框。须用 `platform-detail` / 详情 TAB / 列表绿格综合判断。  
切 TAB、只采实际 TAB、handoff、**三层就绪 / 多项目 iframe / 假 loading**：站点细节见 [sop-detail-tab-refresh.md](sop-detail-tab-refresh.md) SOP-B～K，通用方法见 [ready-signals.md](../../ready-signals.md)。

## 就绪信号（对应 ready-signals 三层，9222 实证 2026-09-07～09-08）

- 层 1 页签激活：`div.active-list.tab-list …` 命中目标 TAB 文案。
- 层 2 侧栏卡片：`div.wrapper ul.list > li.item` 数量 + 首卡 `.item-title` 签名稳定，且标题命中本 TAB 关键字（SOP-C）。
- 层 3 业务区：`el-form-item` ≥ 3 或 label 含业务字段（合同 TAB：合同名称 / 合同金额 / 合同单位 / 合同主要内容），或 `gmd-table-tbody` 已有数据行（SOP-H）。
- 真 loading：可见的 `.gmd-spin-spinning`、可见且非 `display:none` 的 `.el-loading-mask`。
- 假 loading 壳：`.gmd-spin-nested-loading`（常驻 2 个且 `is_displayed=True`，不得当阻塞条件，SOP-K）。

每轮多项目循环、切 TAB、进出详情后都要重新 `get_frame('css:iframe[name=trading-info]')`（SOP-A / SOP-I）。

## 安全边界

- 默认停在保存前：不点击监管网「保存」「提交」「发布」类按钮，不改动公告、台账或合同表单数据（除非用户明确要求）。
- 采集与截图只做只读动作：搜索、切 TAB、点绿格进详情、点侧栏卡片。
- 9222 接管时不 `browser.quit()`、不关闭用户手工打开的 tab，失败后保留现场供下一步继续。

## 定位偏好

优先使用 CSS 候选列表加精确文本：

```json
{
  "action": "click",
  "locator": "css:.gmd-modal .el-tree-node__label",
  "text": "能源电力",
  "timeout": 15
}
```

监管网 `trading-info` 内不要默认依赖 XPath 文本、`tag:*@@text()` 或位置序号。每次 locator/scope 改动后必须从当前失败步骤做 live continuation。
