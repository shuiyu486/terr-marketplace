# 首次同步流程：没有 PLUGIN_FORK_SYNC.md

当目标魔改插件根目录不存在 `PLUGIN_FORK_SYNC.md` 时使用本流程。目标是先安全比较，再为后续同步建立账本。

## 输入确认

需要确认这些信息：

- 本地魔改插件目录。
- 上游插件仓库 URL、分支或 commit、插件子路径。
- 本地 marketplace 仓库 URL 和插件子路径。
- 用户要“只生成计划”“生成账本”“应用低风险更新”中的哪一种；用户确认执行同步/应用后，默认自动提交并 push 本次同步相关改动。

如果缺少上游来源或本地目标路径，先询问用户。不要猜测 URL。

## 建立临时基线

没有账本时无法精确知道上次同步 commit，因此进入审阅模式：

1. 在临时目录获取上游当前版本。
2. 用文件路径和 hash 对比上游当前版本与本地魔改插件。
3. 只读取 hash 不同的文件内容。
4. 把明显本地文件和上游文件分开：例如 `.claude-plugin/plugin.json`、README、本地命令、本地 hook、本地 reference。

如果用户提供了可能的历史 commit/tag，则把它作为候选 `lastSyncedCommit`，但报告中说明这是用户提供的基线。

## 生成 PLUGIN_FORK_SYNC.md

在目标插件根目录创建 `PLUGIN_FORK_SYNC.md`，并把它作为插件所在 git 仓库的正式文件纳入本次同步提交。账本内容要适合跨机器使用：优先写仓库 URL、上游子路径、repo-relative 路径和 plugin-relative 路径，不要写死当前电脑的绝对路径。

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
- path: plugins/<plugin-name>
- pushRemote: origin
- pushBranch: main

## Local modifications
- <relative-path> — <why this file is local/customized>

## Sync policy
- compareStrategy: hash-first
- autoApply: low-risk-only
- pushAfterSync: after-confirmed-sync
```

`Local modifications` 应优先从 hash 差异、README 说明、plugin.json metadata、用户描述中提取。账本是维护清单，不是提交历史记录；只记录仍需长期维护的 fork 差异。如果某个文件已经与上游完全一致，不要把它写入账本，也不要保留它曾经同步或回归上游的原因；这类历史原因应放进 commit message。文件路径用 plugin-relative 形式，例如 `hooks/pretooluse.py`，不要使用本机绝对路径。不要为了填满清单而猜测。

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

只有用户明确同意时，才创建 `PLUGIN_FORK_SYNC.md`。写入后确认它位于目标插件所在 git 仓库内；如果目标插件不在 git 仓库中，先询问用户要纳入哪个本地仓库，不要把账本留成只存在于当前机器的游离文件。如果用户确认执行首次同步/写入账本，写入后默认把 `PLUGIN_FORK_SYNC.md` 纳入本次 commit 并 push；如果工作区不干净、remote/branch 不明确或存在冲突，则停止在提交前并报告原因。
