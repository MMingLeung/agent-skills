# 站点包

通用规则只放在 `references/*.md`。任何带具体选择器、iframe 名、UI 库 class、业务 TAB 名、站点专属流程的内容，都放到 `references/sites/<站点代号>/`。

## 读取顺序

1. 先按 SKILL.md 路由读通用文件；
2. 命中下表任一触发线索，再读该站点包（先 `locator.md`，再 SOP）；
3. 站点包与通用规则冲突时，以站点包的 **live 证据** 为准，并把新证据回写到站点包，不改通用文件。

## 索引

| 代号 | 站点 | 触发线索 | 文件 |
| --- | --- | --- | --- |
| `gd-zbtb` | 广东省招标投标监管网 | 监管网、`gdzbtb`、`iframe[name=trading-info]`、`platform-detail`、节点发布情况、项目台账登记、招标项目信息、中标候选人、合同公示、`gmd-spin` | `locator.md`：作用域表、列表↔详情 locator、三层就绪信号与真/假 loading 元素、安全边界、定位偏好；`sop-detail-tab-refresh.md`：已验证故障表、SOP-A～K（iframe 重取、只采实际 TAB、切 TAB 内容信号、侧栏 locator、列表 vs 详情、handoff 二次连接、9222 验收、三层就绪、每轮重取 iframe、台账轻量采集、假 loading） |

## 一个站点包应包含

按 [templates/site-pack-template.md](../../templates/site-pack-template.md)：

- 作用域表：哪些区域在 root、哪些在哪个 iframe；
- 关键 locator + 后置条件 + live 证据日期；
- 三层就绪信号在本站点对应的元素，真 loading / 假 loading 壳各是什么；
- 站点特有坑 → 硬规则（现象 / 根因 / 规则）；
- 本站点哪些按钮属于保存 / 提交 / 发布（默认不点）。
