# Workspace routing

用于判断当前目录是否是 `terr-marketplace` 仓库，以及实际操作应在哪里进行。

## 仓库定位

`terr-marketplace` 是 Claude Code 插件 marketplace 仓库。

本地仓库通常位于：

- Windows: `~\.claude\plugins\marketplaces\terr-marketplace`
- macOS/Linux: `~/.claude/plugins/marketplaces/terr-marketplace`

当前机器的实际路径以用户说明或文件系统为准。

## 工作目录规则

- 当前工作目录不一定是 marketplace 仓库。
- 修改 marketplace、插件、commands、skills、references 前，先确认实际仓库路径。
- 不要在管理入口目录 clone `terr-marketplace`，除非用户明确要求。
- 涉及 git commit、push、PR 时，必须在真正的 marketplace git 仓库内执行。

## 判断方式

优先检查目标目录是否包含：

```text
.claude-plugin/marketplace.json
plugins/
```

如果需要 git 操作，再确认该目录是 git 仓库且 remote 指向 `shuiyu486/terr-marketplace`。
