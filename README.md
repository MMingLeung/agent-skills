# agent-skills

给在 Cursor、Claude Code 里做交付的人：装上一个技能（一个目录、一份 `SKILL.md`），Agent 就按这份说明把口头需求收成一页，再写界面、文档、浏览器步骤或 Windows 双击启动，并在收工时打开真实产物核对。

## 🚀 三步装好

只装这次要用的一个。`<name>` 换成目录名，例如 `work-doc-writer`。

1. 在仓库根目录执行这一条（装到 Cursor，本机所有项目都能用）：

   ```bash
   cp -R skills/<name> ~/.cursor/skills/<name>
   ```

2. 新开一个对话。已经打开的对话不会重新读刚拷进去的技能。
3. 用日常说法提需求，比如「帮我写操作手册」。说明见 [Cursor Agent Skills](https://cursor.com/docs/skills) 与 [Claude Code skills](https://code.claude.com/docs/en/skills)。

<details>
<summary>Windows、Claude Code、Codex，或只给当前仓库用</summary>

**Claude Code**（用户级；只给当前仓库用则拷到 `.claude/skills/<name>`）

```bash
cp -R skills/<name> ~/.claude/skills/<name>
```

**Windows（PowerShell，Cursor 用户级）**

```powershell
Copy-Item -Recurse skills\<name> $HOME\.cursor\skills\<name>
```

**只给当前 Cursor 仓库用**：拷到项目里的 `.cursor/skills/<name>`。

**Codex**：目标目录改为 `~/.codex/skills/`。

本机如果经常改这些技能，可以用目录联接，让 `~/.cursor/skills/<name>` 指向本仓库的 `skills/<name>`，改一处即生效。

</details>

## 📝 先看输入和输出

开工卡＝动手写代码前，用 4 块内容把需求说清楚的一页纸。目录名是 `demo-kickoff-card`。下面按这个格式走一遍，内容是编的，用来看它长什么样。

你说：

> 样例公告列表上的发布时间，现在是一格一格手工抄。请导出 Excel，列要有标题和发布时间。本机跑，先对上两行。不要提交，不要改正式数据。登录我自己来。

Agent 交出：

```text
【DEMO 开工卡】
背景一句：把样例公告的发布时间，从手工抄写改成本机导出的 Excel。

输入 / 输出：
- 入：本机已打开的样例列表（两行即可）
- 出：Excel，列包括标题、发布时间

人拍板与禁止：
- 只读页面、只写本机文件；禁止提交，禁止改正式数据
- 登录和验证码仍由你本人操作

成功标准：
- DEMO：导出的两行时间，和页面上看到的一致
```

缺了的格子写「待确认」，不编业务规则。

## 👀 收之前和收之后

同一件事，收成那一页之前和之后差在这：

| 收之前 | 收之后 |
| --- | --- |
| 「那个列表的时间帮我弄成表，快点做个演示，别搞正式环境。」 | 背景、输入输出、禁止项、怎样算演示成功，四块分开 |
| 「别搞正式环境」藏在句尾 | 「禁止提交、禁止改正式数据」单独成行，可以改字 |
| 没写要对上哪几行 | 写明导出两行，时间与页面一致 |

三十秒可以自己贴一次。新开对话，粘贴下面这段：

```text
先别写代码。把下面几句收成一页四块清单：背景一句、输入输出、谁拍板和禁止做什么、怎样算演示成功。缺的写待确认。

要点：样例公告列表上的发布时间，现在是手工抄。要导出 Excel。本机跑。不要提交，不要改正式数据。先对上两行就行。
```

贴完应看到四块都在的清单。若它开始写代码，补一句：先出这页，缺的写待确认。

## 🧭 按场景选

我想做下面这些事时，用对应的技能。一次任务通常只对上其中一两个。

- 我想先把口头需求说清楚，再写代码。用 [`demo-kickoff-card`](skills/demo-kickoff-card/)
- 我想让浏览器按步骤点页面，把列表抓下来。用 [`drission-crawler`](skills/drission-crawler/)
- 我想让别人双击就能打开桌面程序。用 [`windows-gui-bat-launcher`](skills/windows-gui-bat-launcher/)
- 我想把内部系统的表单、表格、查询做正式一点。用 [`government-service-design`](skills/government-service-design/)
- 我想写操作手册、说明书或成果报告。用 [`work-doc-writer`](skills/work-doc-writer/)
- 我想给毕业论文 Word 排版。用 [`word-thesis-format`](skills/word-thesis-format/)
- 我想收工前打开真实结果核对。用 [`dev-review-verify`](skills/dev-review-verify/)
- 我想把这次改了什么留给下一个人。用 [`dev-process-handoff`](skills/dev-process-handoff/)

## 📋 技能一览

| 技能 | 一句话作用 | 你会这样说 | 示例 |
| --- | --- | --- | --- |
| [`demo-kickoff-card`](skills/demo-kickoff-card/) | 写代码前把口头需求收成一页四块清单，也就是上面的开工卡。 | 「刚跟业务聊完，先整理成一页，先别写代码。」 | 背景一句；输入 / 输出；谁拍板和禁止项；怎样算演示成功。 |
| [`drission-crawler`](skills/drission-crawler/) | 用 DrissionPage 操作真实浏览器：先等页面，再定位、点击，然后读回结果；失败留下证据。已含广东省招标投标监管网（gd-zbtb）规则包。 | 「这个页面点了没反应，用 DrissionPage 把列表抓下来。」 | 每一步记下等待、定位和回读；不行就重试或停。 |
| [`windows-gui-bat-launcher`](skills/windows-gui-bat-launcher/) | Windows 上双击 bat 打开桌面程序：黑框提示请稍候，窗口出来后黑框自己关掉。 | 「双击闪退，黑框等窗口出来再自己关。」 | 窗口显示后写 `.ready_` 标记，bat 看到就退出。 |
| [`government-service-design`](skills/government-service-design/) | 政务或企业内部后台：白底浅灰，表单、表格、查询和办理优先，文案短。 | 「这个后台要政务感，表单和表格弄清楚。」 | 没指定颜色时主按钮用 `#0A4CB5`，按钮写「查询」「保存」。 |
| [`work-doc-writer`](skills/work-doc-writer/) | 对照程序源码写操作手册、技术说明或成果报告（Word），截图可以加红框。 | 「帮我写操作手册。」 | 按钮名称用界面上的原文，再生成 docx。 |
| [`word-thesis-format`](skills/word-thesis-format/) | 把毕业论文 Word 排成固定版式。 | 「这篇毕业论文按学校格式排一下。」 | A4，页边距 25 mm，正文小四宋体加 Times New Roman，1.5 倍行距，标题黑体。 |
| [`dev-review-verify`](skills/dev-review-verify/) | 收工前打开真实产物再核对。LIVE 验收＝用真实环境打开这次做出的文件再核对，单测通过不能代替。 | 「pytest 绿了还不算完，打开结果对一下。」 | 单测和 sync（同步交付包）之后还要实跑。回复里分开写单测、打开了哪份文件、交付包有没有跑。有本机验收备忘就按备忘跑；没有索引就不向你要一份公开仓库里不存在的文件。 |
| [`dev-process-handoff`](skills/dev-process-handoff/) | 行为、接口、默认值或验收标准变了，就写给下一个人。交接＝把改了什么、以什么为准、怎样算做完写进文档。 | 「默认值改了，更新交接，别只留在聊天里。」 | 更新 `CURRENT_HANDOFF.md`：变更摘要、以哪份为准、怎样算做完。 |

## 🎬 从这句话走到能交出去

还是上面的发布时间。四个技能接在同一件事上。

1. 你说：「先别写代码，整理成一页。」得到开工卡，四块都在。你改掉不对的格子。
2. 你说：「按这页做演示。」抓网页走 `drission-crawler`：等列表出现，定位发布时间，读回来，写入 Excel。做的是窗口，就改走 `government-service-design` 或 `windows-gui-bat-launcher`。
3. 你说：「跑两行再算完。」按 `dev-review-verify` 做 LIVE 验收：打开页面，打开导出的 Excel，看两行时间一致。
4. 你说：「写给下一个人。」按 `dev-process-handoff` 做交接，在 `CURRENT_HANDOFF.md` 写下改了什么、禁止改正式数据、怎样算这两行通过。

## 🗺️ 技能怎么串起来

多数任务是一条线：先把口头需求收成一页，再按任务选一个技能实现，然后用真实环境验收，行为有变化就写交接。中间那一步按任务选，不必每个技能都走。

```mermaid
flowchart LR
  kickoff["demo-kickoff-card<br/>先整理一页清单"] --> build["按任务选一个技能<br/>实现"]
  build --> review["dev-review-verify<br/>真实环境跑一遍"]
  review --> handoff["dev-process-handoff<br/>写下交接"]
```

按任务选用：`drission-crawler`、`windows-gui-bat-launcher`、`government-service-design`、`work-doc-writer`、`word-thesis-format`。

## ❓ 常见问题

**要一次装完全部吗？**
不用。用哪个装哪个。装太多，每次对话都要多读一段说明。

**装完还是老样子？**
新开一个对话再提需求。也可以点名目录，例如「用 demo-kickoff-card」。

**开工卡、LIVE 验收、交接各是什么？**

- 开工卡＝动手写代码前，用 4 块内容把需求说清楚的一页纸。
- LIVE 验收＝用真实环境打开这次做出的文件再核对，例如导出的 Excel、双击打开的窗口。
- 交接＝把这次改了什么、以哪份说明为准、怎样算做完，写进给下一个人的文档。

**仓库里为什么没有 `INDEX.md`？**
`dev-review-verify` 的 `references/projects/INDEX.md` 是本机验收备忘（原名：配方卡），里面是本机路径、命令和产物位置，不进公开仓库。克隆下来没有这个文件是正常的，技能会改看当前仓库的 `AGENTS.md`、`CURRENT_HANDOFF` 和 `scripts/*live*`。

**这些技能会自动改正式系统吗？**
开工卡里会写明禁止项。浏览器采集默认不保存、不提交、不发布网页表单。

**和 DrissionPage 是什么关系？**
只有 `drission-crawler` 使用它。文档、界面、启动、验收和交接各自一份技能。

## 🔧 改这个仓库时

这些技能从真实交付里抽出来。改的时候按下面几条，避免把本机路径和真实数据提交上去。

- 通用规则放在技能根目录的 `SKILL.md` 和 `references/`。某个网站专用的选择器和步骤放在 `references/sites/<代号>/`。
- 不提交 `output/`、真实截图、`.env`、Cookie。
- 新网站按 [`templates/site-pack-template.md`](skills/drission-crawler/templates/site-pack-template.md) 建包，并更新本页的技能表。
- 某个项目的验收备忘记在 `dev-review-verify/references/projects/<代号>/`，只留在本机。入库的只有 [`README.md`](skills/dev-review-verify/references/projects/README.md) 和 [`_template/`](skills/dev-review-verify/references/projects/_template/)。
- 交付包资源完整性检查脚本：[`check_delivery_resources.py`](skills/dev-review-verify/scripts/check_delivery_resources.py)。
- 本机可以用目录联接，让 `~/.cursor/skills/<name>` 指向本仓库 `skills/<name>`，改一处即生效。

每个技能有 `evals/evals.json`：约 3 条应触发、2 条不应触发。字段沿用常见 skill eval（`skill_name`、`evals`、`id`、`prompt`、`expected_output`、`assertions`），并加 `should_trigger` 区分是否该启用本技能。

## ⚠️ 许可和注意事项

### DrissionPage

`drission-crawler` 使用上游 [DrissionPage](https://github.com/g1879/DrissionPage)。上游许可限制商业使用：个人可以用于学习和合法非盈利；未获版权持有人授权，不得把源码或二进制用于商业行为。以 [LICENSE](https://github.com/g1879/DrissionPage/blob/master/LICENSE) 为准。这里不粘贴许可全文。

### 使用范围

和具体网站有关的技能，只记录公开页面上怎样定位、怎样等页面稳定。默认不保存、不提交、不发布表单。使用时须遵守目标网站的条款和当地法律。
