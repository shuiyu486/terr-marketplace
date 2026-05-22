# 已有账本更新流程：存在 PLUGIN_FORK_SYNC.md

当目标魔改插件根目录存在 `PLUGIN_FORK_SYNC.md` 时使用本流程。目标是按账本精确做三方对比，并安全移植上游变化。

## 读取账本

从 `PLUGIN_FORK_SYNC.md` 提取：

- `Upstream.repo/path/branch/lastSyncedCommit`
- `Local plugin.repo/path/pushRemote/pushBranch`
- `Local modifications`
- `Sync policy.compareStrategy/autoApply/pushAfterSync`

账本中的 `Local plugin.path` 应是 repo-relative 路径，例如 `plugins/<plugin-name>`；`Local modifications` 应是 plugin-relative 路径，例如 `hooks/pretooluse.py`。如果读到账本里有本机绝对路径，更新账本时顺手转换为可移植路径。

如果 `lastSyncedCommit` 缺失或明显不是 commit/tag，停止自动更新，改走首次同步流程或询问用户补充。

## 三方快照

准备三份快照：

| 快照 | 来源 |
| --- | --- |
| `base` | upstream repo 的 `lastSyncedCommit` + upstream path |
| `upstream` | upstream repo 的当前 branch/head + upstream path |
| `local` | 本地插件目录 |

不要在本地插件目录直接执行 destructive git 操作。

## hash-first 对比

先生成三份快照的文件 hash 清单：

1. `base == upstream`：上游未改，通常不需要读文件。
2. `base == local`：本地未改，上游变化可作为低风险候选。
3. `base != upstream` 且 `base != local`：双方都改，列为冲突并读取内容审阅。
4. `Local modifications` 中列出的文件始终高亮展示，即使 hash 分类显示低风险。

## 文件级分类

| 类型 | 判断 | 默认处理 |
| --- | --- | --- |
| 仅上游变更 | `base→upstream` 有变，`base→local` 无变 | 可自动移植到补丁 |
| 仅本地变更 | `base→local` 有变，`base→upstream` 无变 | 保留本地 |
| 双方同文件变更 | 两边都改同一文件 | 人工审阅 |
| 上游删除、本地修改 | 上游删除但本地仍改 | 高风险冲突 |
| 本地新增 | 只存在 local | 保留 |
| 上游新增 | 只存在 upstream | 可建议新增 |

`PLUGIN_FORK_SYNC.md` 是本地维护账本，不来自上游；除非用户要求更新账本，否则不要纳入上游同步补丁。账本是维护清单，不是提交历史记录；只记录仍需长期维护的 fork 差异。如果某个文件已经与上游完全一致，不要把它列为本地魔改文件，也不要保留它曾经同步或回归上游的原因；这类历史原因应放进 commit message。账本文件本身应作为目标插件仓库中的受版本控制文件维护，更新账本时默认纳入本次同步提交。

## 更新报告

输出结构要便于阅读，优先使用醒目标记、短结论和表格：

```markdown
## 重点结论
- 🚨 高风险：<冲突、删除、本地魔改被上游同文件修改等；没有则写“无”。>
- ⚠️ 需确认：<最需要用户判断的一件事；没有则写“无”。>
- ✅ 可自动同步：<可安全移植的上游变更；没有则写“暂无”。>
- ℹ️ 当前模式：已有账本更新，`<base>` → `<head>`。

## 账本摘要
| 项目 | 内容 |
| --- | --- |
| 上游 | `<repo>/<path>` |
| 基线 | `<lastSyncedCommit>` |
| 当前上游 | `<head>` |
| 本地插件 | `<repo-relative-path>` |
| 本地魔改文件 | `<file>`、`<file>` |

## 上游变化摘要
| 类型 | 数量 | 重点文件 |
| --- | ---: | --- |
| 新增 | <n> | `<file>`、`<file>` |
| 修改 | <n> | `<file>`、`<file>` |
| 删除 | <n> | `<file>`、`<file>` |

## 文件级同步计划
| 文件 | 差异类型 | 风险 | 建议 | 原因 |
| --- | --- | --- | --- | --- |
| `<path>` | 仅上游变更/仅本地变更/双方同文件变更/删除冲突 | 🚨/⚠️/✅ | 应用上游/保留本地/人工确认/更新账本 | <一句话说明依据> |

## 待用户确认
- [ ] 是否生成补丁。
- [ ] 是否应用低风险变更。
- [ ] 是否更新最近同步基线。

确认应用同步后，默认自动 commit 并 push 本次同步相关改动；不再把提交/push 作为单独确认项。
```

如果差异很多，只展示重点差异和统计；不要把大量 diff 直接塞进报告正文。

报告前做一次排版自检：最终回复必须保留上面的小节标题和文件级同步计划表格。即使上游没有变化、插件已经最新，或用户只是问“是不是最新”，也要用该结构说明“无可同步变更”。

## 应用更新

只有用户明确同意时才写入文件。应用低风险变更后：

- 更新 `PLUGIN_FORK_SYNC.md` 的 `lastSyncedCommit` 为已同步的 upstream head commit。
- 如果发现新的本地魔改文件，同步更新 `Local modifications`，并使用 plugin-relative 路径。
- 如果账本中存在本机绝对路径，转换为 repo-relative 或 plugin-relative 路径。
- 运行可用的最小验证，例如 JSON 解析、SKILL.md frontmatter 检查、`claude plugin validate <marketplace>`。

## commit/push 条件

用户确认执行同步/应用更新后，自动提交并 push 本次同步相关改动，不再单独追问 commit/push。只有同时满足以下条件才执行：

- 工作区只包含本次同步相关改动，包括生成或更新的 `PLUGIN_FORK_SYNC.md`。
- 已展示提交文件列表、提交信息、目标 remote/branch。
- 无未解决冲突或高风险自动改写。
- remote 和 branch 明确可用。

提交信息必须说明“为什么”：

- 对回归上游的文件，说明回归原因；如果能取得 upstream commit message，引用或概括它。
- 对保留本地魔改的文件，说明保留原因。
- 如果无法取得 upstream commit message，写明依据来自文件 diff、账本或用户确认。

如果任一条件不满足，停止在提交前并报告需要用户处理的具体问题。
