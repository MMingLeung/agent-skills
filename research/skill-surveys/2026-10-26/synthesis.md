# 2026-10-26 综述

当日阅读 5 个仓库，均为 2026-10-26 能打开、具有 `SKILL.md` 或等价技能目录的公开项目。星标为当日 GitHub API `stargazers_count`。

| 笔记 | 仓库 | 星标 | 许可（查阅所见） | 类型 |
| --- | --- | --- | --- | --- |
| [anthropics-skills.md](anthropics-skills.md) | [anthropics/skills](https://github.com/anthropics/skills) | 183889 | 多数示例为 Apache 2.0；docx/pdf/pptx/xlsx 为 source-available，docx 为专有条款 | 官方技能库（含文档、沟通、写技能） |
| [obra-superpowers.md](obra-superpowers.md) | [obra/superpowers](https://github.com/obra/superpowers) | 305366 | MIT | 编程代理的整套方法 |
| [nuwa-skill.md](nuwa-skill.md) | [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) | 36083 | MIT | 人物思维蒸馏 |
| [huashu-design.md](huashu-design.md) | [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design) | 26461 | MIT | 视觉交付（原型、幻灯片、动画） |
| [cangjie-skill.md](cangjie-skill.md) | [kangarooking/cangjie-skill](https://github.com/kangarooking/cangjie-skill) | 11760 | MIT | 把书和长材料蒸馏成技能 |

## 写法上的共同点

五份材料都把「何时启用」写进 description，而不是只放在正文标题里。长仓库都把入口写短：官方内部沟通技能按文种打开 `examples/`，花叔设计按模块打开手册，仓颉按阶段打开 `methodology/`，女娲把模板和评分卡放在 `references/`。

另一处共同点是验收不信任作者自述。superpowers 要求当次验证输出；女娲要求另一个代理按公开事实评分；仓颉要求代表任务真的做完；官方 skill-creator 要求带技能和基线对照。花叔设计把检查点落成文件，文件缺失即视为步骤未做。

人物蒸馏和拆书还共享一套内容纪律：材料不够就标明推断或降级，不把缺口写成事实。这和本库开工卡里的「待确认」是同一条，只是他们用在人物和书籍上。

## 设计意图

这些仓库默认模型会跳步、会用通用腔、会在没证据时宣布完成。所以规则写成门禁和反例，而不是原则段落。

技能拆分则服务检索。仓颉的晋级门和花叔的路由表都在控制「顶层名字」的数量。名字太多，description 互相遮盖，不该调用的技能会被叫起来。官方库用独立目录加许可字段，把可复用示例和不可复用的文档实现隔开。

女娲和仓颉的意图是生产新技能。superpowers 和花叔设计的意图是管住一次任务的过程。本库现有八个技能属于后者里的交付过程，不是技能工厂。

## 对本库可抄的部分

可抄的是纪律，落在已有文件上，不新开技能名。

1. **触发句继续带负例。** `demo-kickoff-card`、`drission-crawler`、`work-doc-writer`、`government-service-design`、`dev-review-verify` 的 description 已写不用场景。以后改技能时保持负例留在 frontmatter，并在 `evals.json` 里保留不该触发的样本。
2. **入口与手册分离。** `government-service-design` 的色值和文案细则、`drission-crawler` 的站点包、`work-doc-writer` 的三种模板，继续留在引用和模板目录。`SKILL.md` 只保留路由、硬规则和停手条件。
3. **检查点以文件为准。** `dev-review-verify` 的 LIVE 和 `drission-crawler` 的失败证据，以路径上的产物为准。对话中的「已核对」不算数。
4. **完成声明绑定当次证据。** 收工顺序维持：单测和同步可以先做，LIVE 放在最后。未做 LIVE 时结论写未验收完成。这与 superpowers 的验证门禁同向，用本库已有表述即可。
5. **粒度用晋级门自查，而不是按外部仓库拆分。** 新站点进 `drission-crawler` 的站点包。只有两套流程的触发已经冲突，才新增顶层技能。开工卡不拆成多张技能，工作文档不按章节拆成多份技能。

## 对本库不抄的部分

1. **不把人物蒸馏写入交付技能。** 不增加角色、口吻、表达指纹、多代理调研或保真度评分。周报、手册、界面文案仍按岗位和界面原文写。
2. **不把拆书流水线写入仓库。** 不新增 Bundle、能力卡编译和书籍阶段文件。`work-doc-writer` 的事实来源是源码和截图，不是书。
3. **不把视觉三方向和风格库写入政务界面。** `government-service-design` 保持一套克制规范。指定了颜色就用指定色，未指定就用已定主色。营销页继续明确排除。
4. **不把通用编程方法整套套到浏览器和启动脚本上。** 不要求每步 2 到 5 分钟的实现计划，不要求会话一开始禁止澄清，不把子代理红绿重构写成 `drission-crawler` 或 `windows-gui-bat-launcher` 的步骤。
5. **不复制 Anthropic 专有文档技能。** `docx`、`pdf`、`pptx`、`xlsx` 的脚本和提示不进入 `work-doc-writer` 或 `word-thesis-format`。Word 仍走本库模板、检查脚本和预览。

## 若以后改现有技能，优先动哪里

本次只记阅读结论，不改 `skills/`。

- `demo-kickoff-card`：保持四块和一轮确认。复述范围可以留在开做前的两行，不扩展成设计说明书。
- `drission-crawler`：禁止项旁边保持停手条件；新网站用站点包。不引入并行代理操作页面。
- `dev-review-verify`：常见「看起来完成了」的说法（只跑了 pytest、只有探针文本、没有打开产物）继续写成不能收工的条件。
- `work-doc-writer`：入口可以再明确「先判定手册 / 说明书 / 成果报告，再打开对应模板」。不替换实现。
- `government-service-design`：维持何时用、何时不用。不增加方案竞选。
- `dev-process-handoff`：继续写行为、默认值和验收变化。不写个人风格账本，也不写技能自动进化接口。
