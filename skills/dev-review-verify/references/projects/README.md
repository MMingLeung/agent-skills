# 项目包（本机专用）

项目包记录某个项目的 LIVE 配方卡：测试数据路径、LIVE 命令、产物位置、通过标准、交付包约定。
里面是本机绝对路径和项目信息，**不入公开仓库**（`.gitignore` 已排除本目录下除 `README.md`、`_template/` 外的所有内容）。

## 目录

```text
references/projects/
├─ README.md          本文件（入库）
├─ _template/         新建项目包的模板（入库）
├─ INDEX.md           本机项目包索引（不入库）
└─ <代号>/            某项目的包（不入库）
   ├─ live-recipes.md 配方卡
   └─ delivery.md     交付包、sync 命令、资源检查参数（有交付包时）；路径通例见上一级 [../delivery-layout.md](../delivery-layout.md)
```

通用「交付根 vs 子包根」写在入库文件 [../delivery-layout.md](../delivery-layout.md)；项目包 `delivery.md` 只补本机路径与 sync 表，勿把可复用通例只写在本机包里（否则无法进 GitHub）。


## 新建项目包

1. 复制 `_template/` 为 `<代号>/`，代号用短英文。
2. 按 [../../templates/live-recipe-card.md](../../templates/live-recipe-card.md) 填卡，只写有证据的路径和命令。
3. 在 `INDEX.md` 加一行：代号、触发线索（工作区路径关键字、仓库名、交付目录名）、入口文件。

`INDEX.md` 不存在时按下面格式新建：

```markdown
# 本机项目包索引

| 代号 | 触发线索（路径 / 仓库名 / 交付目录名，命中任一） | 入口 |
| --- | --- | --- |
| demo | my-repo、my-repo-delivery、业务关键词 | [demo/live-recipes.md](demo/live-recipes.md) |
```

## 维护

- 用户给了新样例、改了测试数据位置 → 当次任务里更新对应卡。
- 卡里的命令跑不通 → 先修卡再收工，不留失效的卡。
