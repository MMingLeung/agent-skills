# 站点包 gd-zbtb：详情 TAB / 侧栏列表刷新与二次连接

> 站点：广东省招标投标监管网「节点发布情况 / 项目台账登记」。live 实证沉淀。  
> 通用判定方法（分层就绪、内容信号、假 loading、每轮重取 frame、列表 vs 详情）见 [ready-signals.md](../../ready-signals.md)；本文只记本站点的选择器、TAB 名和坑。  
> 适用：Vue 详情多 TAB、侧栏卡片列表、Engine CONFIG 结束后再开 Python 采集、9222 双连接、台账轻量采集。

## 已验证故障 → 硬规则

| 现象 | 根因 | SOP |
| --- | --- | --- |
| `切换TAB失败: 未找到详情 TAB: 中标结果` | 假定每个项目都有完整 TAB | **只轮询页面实际存在的 TAB**；缺失静默跳过，不写失败行 |
| 节点名串成「招标文件」/ 旧卡片日期 | 页签已亮，侧栏未刷新就采 | **激活态不够**；必须等内容像本 TAB |
| 日期相同的不同 TAB 怕误判 | 误用「日期变化」当刷新条件 | **日期可相同**；靠标题关键字 / 标题集合 |
| CDP `querySelectorAll("li.item")` 超时 | 全页扫 `li.item` + 高频轮询 + 旧 frame | **作用域收窄** + 切页后重取 iframe + 轻量签名 |
| GUI 登录成功后立刻 `get_frame` 报错 | Engine 刚结束又二次 `Chromium(9222)`；或详情页搜索框被当成列表 | **handoff settle**；用详情特征区分列表；吞 ElementNotFound 再 poll |
| 日志长时间空白 | 采集线程未把 stdout 接到 GUI | **进度 print + 把 stdout/stderr 接到 GUI 日志队列** |
| **第 2 个项目搜索框空、列表未过滤** | 上一项目停在详情，**复用旧 frame** 写搜索 | **SOP-I**：每轮搜索前软重取 `trading-info` |
| **招标项目信息 / 合同等 40～60s 空等** | 用侧栏首卡（常为「…招标文件」）当就绪 | **SOP-H**：右侧**业务表单**优先于侧栏首卡 |
| **详情落地 20s 超时** | 入口 TAB 侧栏长期「…招标文件」，强行等项目名首卡 | **SOP-H**：入口只等 TAB+侧栏稳定；目标字段在**目标 TAB 表单**判定 |
| **合同截图表单已出仍等满 25s「loading」** | `gmd-spin-nested-loading` 常驻且 `displayed=true` | **SOP-K**：只认 `gmd-spin-spinning` / 可见 `el-loading-mask` |
| **合同截图过早（空白）** | 只等 TAB/侧栏，不等右侧只读表单 | **SOP-H**：`el-form-item` / 业务 label 可见后再 `captureScreenshot` |

## SOP-A：DrissionPage 与 iframe（澄清）

DrissionPage **免的是 Selenium `switch_to.frame` 式上下文切换**，不是「父页面直接点 iframe 内元素」。

```text
frame = tab.get_frame(locator)   # 或遍历 get_frames 按 name/url 识别
→ 所有列表/详情业务动作都在 frame 上做
→ 切页 / 导航 / 重绘后禁止复用旧 frame；重新 get_frame
```

`get_frame` 失败时：

1. 捕获 `ElementNotFoundError` / timeout，返回空并 poll；
2. 过滤 `NoneElement` 假成功；
3. 多 locator：`css:iframe[name=…]`、`xpath://iframe[@name=…]`、`get_frames()` 回退；
4. 超时再抛**可读** `RuntimeError`（带 tab_url），不要把原始 CDP 异常直接当业务结论。

## SOP-B：只采「实际存在」的 TAB

```text
读取可见 TAB 文案列表（去重）
→ 按已知业务顺序排列；未知 TAB 追加在后
→ 缺失的固定 TAB 跳过，不记「未找到 TAB」
```

禁止用完整枚举硬遍历「每个项目都应有的 TAB」。

## SOP-C：切 TAB 后置条件（核心）

```text
记录切页前卡片 payload（标题集合为主；可含日期/状态）
→ 点击目标 TAB
→ **软取** trading-info / 当前 iframe（失败只 sleep+poll，禁止每轮硬等 TIMEOUT）
→ 等待 active-list（或等价激活态）== 目标 TAB
→ 内容就绪：
     · 本次轮询的首个实际 TAB：激活 + 卡片签名稳定 + 拒绝其它 TAB 残留标题
       （例：招标项目信息不得含「招标文件|投标文件|…」）
     · 后续有业务关键字的 TAB：卡片标题命中本 TAB 关键字
       （例：中标候选人 TAB 必须含「中标候选人|评标报告」，
        残留「投标文件公示」一律未就绪）
     · 后续无关键字 TAB：标题集合相对切页前变化
→ 连续稳定 N 次（poll）后才采集
→ 超时：重试点击一次；仍失败则跳过并记**区分备注**
   （丢失 iframe / 卡片未刷新 / 其它），禁止入库串数据
```

硬禁止：

- 仅 `sleep(0.8)` 当切页成功；
- 激活后未变内容也采集；
- 用「发布日期是否变化」当唯一刷新条件（**日期相同的不同 TAB 合法**）。

分类归节点时：

- 独占 TAB：以页签为准；
- 合并 TAB：只认本 TAB 域内关键字；旧标题关键字不得串节点。

## SOP-D：侧栏卡片 locator

优先：

```text
css:div.wrapper ul.list > li.item
→ .item-title / .desc-time / .desc-status
```

禁止默认全页 `css:li.item`（易扫到无关节点、拖垮 CDP）。

settle 阶段用**轻量签名**（张数 + 首卡标题 [+ 日期]），不要每 300ms 全量深挖整表。

## SOP-E：列表 vs 详情（入口误判）

详情页也可能有「招标项目名称」搜索框。判断「已在列表」必须同时满足：

```text
有搜索框
AND 非 platform-detail URL
AND 无详情 TAB 条（或有列表状态格 span.tendering）
```

已在列表：不要无条件 `tab.get(列表URL)`。  
在详情：再导航回列表，并等搜索框 + 列表信号。

## SOP-F：Engine / CONFIG 结束后二次 Python 采集（handoff）

```text
CONFIG run 成功（pause 确认列表）
→ 短暂 settle（页面/CDP 收尾）
→ 新建 Chromium(9222)（注意可能与刚结束的 Engine 连接竞态）
→ 按 URL 选监管网 tab，不要盲信 latest_tab
→ 再 get_frame / 采数
```

GUI 采集线程必须把 stdout/stderr 接到日志队列，并输出：

```text
当前项目 i/n
当前 TAB j/m 与名称
正在等什么（激活 / 关键字 / 标题变化）
当前首卡预览
本 TAB 采到几行
```

无进度日志时，禁止把「卡住」只归因于业务，先查日志链路。

## SOP-G：9222 验收话术

- 单元测试 / GUI 文案 ≠ live 成功。
- live 至少证明：实际 TAB 集合、切 TAB 后首卡标题随 TAB 变化、无串节点、无全页 `li.item` CDP 超时。
- 默认不保存、不提交、不发布。

## SOP-H：三层就绪信号（侧栏 / 表单 / loading）

监管网详情页常**三层异步**，禁止混为一层判定：

```text
层 1  页签激活（active-list == 目标 TAB）
层 2  侧栏卡片（li.item 标题 / 签名稳定）
层 3  右侧业务区（表单 label、el-form-item、只读详情、表格行）
```

硬规则：

1. **截图 / 入库 / 回读字段** 以 **层 3** 为准；层 1、2 只能作辅助，不能单独通过。
2. **入口落地**（点绿格后）：层 1 + 层 2 稳定即可进入下一动作；**不要**在入口 TAB 强行要求侧栏首卡等于「项目名本身」（从合同列进详情时首卡常为「…合同信息公开」）。
3. **切到目标 TAB 后**：若层 3 未出、层 2 已有卡，可**点侧栏首卡**触发右侧加载，再 poll 层 3。
4. 层 3 已可见时，**不得**再被层 2 的「首卡不像本 TAB」阻塞到超时（例：招标项目信息用表单 label 就绪即可采）。

层 3 探测示例（合同 TAB，9222 实证）：

```text
label 含：合同名称 / 合同金额 / 合同单位 / 合同主要内容 …
或 el-form-item 数量 ≥ 3
或 gmd-table-tbody 已有数据行
```

日志须区分：`页签未激活` / `侧栏未刷新` / `表单未渲染` / `假 loading 拦截`（见 SOP-K）。

## SOP-I：多项目列表搜索 — 每轮重取 iframe

```text
for 每个项目:
  回到列表页（必要时导航）
  frame = 重新 get_frame('css:iframe[name=trading-info]')   # 禁止沿用上一项目详情页的 frame 引用
  写搜索框 → 回读 value
  点「查询」
  等行集合变化或仅剩命中行
  …
```

症状：第 2 个项目起搜索框空、列表多行未过滤、截图仍是上一项目。  
根因：在 **platform-detail** 详情 scope 上对过期 frame 调 `ele/input`。

## SOP-J：台账轻量采集（列表 + 仅合同 TAB）

仅需登记表时，不要遍历全部详情 TAB：

```text
列表：搜索 → 读绿/红 √× → 列表窗口截图（点绿格前）
若列表合同计数 > 0：
  优先点「项目合同及履行公示」列绿格（无则回退第一个绿格）
  入口落地（SOP-H 层 1+2）
  仅切/确认合同 TAB → 等层 3（SOP-H）→ 合同窗口截图 + 读侧栏卡标题
若合同计数 == 0：不进详情，已发合同标段写 0
```

禁止：为 √× 去点招标公告/招标文件等 TAB（列表已足够）。

## SOP-K：假 loading（`nested-loading` 壳）

GMD / Element 表格区常残留：

```text
.gmd-spin-nested-loading   # 容器壳，可能长期 is_displayed=true
.gmd-spin-spinning         # 真正转圈，才算 blocking loading
.el-loading-mask           # 须可见且 style 非 display:none
```

```text
blocking_loading(frame):
  仅当存在可见的 .gmd-spin-spinning
  或可见的 .el-loading-mask（排除 display:none）
  返回 true

panel_ready(frame):
  先检测层 3 业务内容（SOP-H）
  若层 3 已 true → 直接 ready，忽略 nested-loading 壳
  否则再判 _blocking_loading
```

9222 诊断命令（修改判定策略前必跑）：

```python
len(frame.eles("css:.gmd-spin-nested-loading"))
len(frame.eles("css:.gmd-spin-spinning"))
len(frame.eles("css:.el-form-item"))
# nested-loading 常为 2 且 displayed=true，但 form-item 已有 30+
```
