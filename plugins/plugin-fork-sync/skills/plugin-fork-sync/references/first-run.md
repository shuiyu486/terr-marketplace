# 首次同步流程：没有 PLUGIN_FORK_SYNC.md

当目标魔改插件根目录不存在 `PLUGIN_FORK_SYNC.md` 时使用本流程。目标是先安全比较，再为后续同步建立账本。

## 输入确认

需要确认这些信息：

- 本地魔改插件目录。
- 上游插件仓库 URL、分支或 commit、插件子路径。
- 本地 marketplace 仓库 URL 和插件子路径。
- 用户要“只生成计划”“生成账本”“应用低风险更新”“提交/push”中的哪一种。

如果缺少上游来源或本地目标路径，先询问用户。不要猜测 URL。

## 建立临时基线

没有账本时无法精确知道上次同步 commit，因此进入审阅模式：

1. 在临时目录获取上游当前版本。
2. 用文件路径和 hash 对比上游当前版本与本地魔改插件。
3. 只读取 hash 不同的文件内容。
4. 把明显本地文件和上游文件分开：例如 `.claude-plugin/plugin.json`、README、本地命令、本地 hook、本地 reference。

如果用户提供了可能的历史 commit/tag，则把它作为候选 `lastSyncedCommit`，但报告中说明这是用户提供的基线。

## 生成 PLUGIN_FORK_SYNC.md

建议内容：

```markdown
# Plugin Fork Sync

## Upstream
- repo: <upstream-repo-url>
- path: <upstream-plugin-path>
- branch: <branch>
- lastSyncedCommit: <commit-or-needs-confirmation>

## Local plugin
- repo: <local-marketplace-repo-url>
- path: <local-plugin-path-in-repo>
- pushRemote: origin
- pushBranch: main

## Local modifications
- <relative-path> — <why this file is local/customized>

## Sync policy
- compareStrategy: hash-first
- autoApply: low-risk-only
- pushAfterSync: ask
```

`Local modifications` 应优先从 hash 差异、README 说明、plugin.json metadata、用户描述中提取。不要为了填满清单而猜测。

## 首次同步报告

输出结构：

```markdown
## 结论
- 当前模式：首次同步/无账本
- 是否能安全自动移植：否/部分
- 建议下一步：确认账本、再执行更新

## 已识别来源
- 上游：repo/path/ref
- 本地：repo/path

## 差异摘要
- 仅本地存在：...
- 上游存在但本地不同：...
- 可能是本地魔改：...

## 建议写入的 PLUGIN_FORK_SYNC.md
```markdown
...
```

## 待确认
- [ ] lastSyncedCommit 是否正确
- [ ] Local modifications 是否完整
- [ ] 是否写入 PLUGIN_FORK_SYNC.md
- [ ] 是否继续应用低风险更新
```

## 写入规则

只有用户明确同意时，才创建 `PLUGIN_FORK_SYNC.md`。写入后不要自动 commit/push，除非用户明确要求。
