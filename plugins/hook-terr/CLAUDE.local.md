# CLAUDE.local.md — hook-terr 插件维护入口

本目录用于维护 `hook-terr`，一个可扩展的 Claude Code hook runtime 插件。

## 重要原则

- 本目录用于维护、迭代 `shuiyu486/terr-marketplace` 中的 `hook-terr` Claude Code 插件；当前会话目录不一定是 marketplace git 仓库。
- 不要在当前目录 clone `terr-marketplace`，除非用户明确要求。
- 真正修改 marketplace 或插件时，优先在本地 marketplace 仓库根目录操作。
- 插件源码、默认配置、presets 和文档都通过 `terr-marketplace` 分发。
- 用户全局目录和项目目录只作为覆盖层，不是发布源。
- 修改 hook 协议、规则 schema、通知命令或 marketplace 注册前，按下方路由读取对应 reference。
- 只读取当前任务命中的 reference 文件；不要预读整套 references。

## 仓库定位

本地 marketplace 仓库通常位于：

- Windows: `~\.claude\plugins\marketplaces\terr-marketplace`

判断真实仓库时优先检查：

```text
.claude-plugin/marketplace.json
plugins/
```

## 同步规则

- 本文件需要在当前工作目录与本地 marketplace 仓库根目录保持同步。
- 修改任一处 `CLAUDE.local.md` 后，同步另一处。
- 远程仓库中的 `CLAUDE.local.md` 通过 marketplace 仓库提交和推送同步。

## 按需加载路由

| 任务意图 | 读取文件 | 不读取时 |
|---|---|---|
| 修改 runtime、hook 入口、事件流 | `references/runtime.md` | 只改 README、示例或 marketplace 文案 |
| 修改 settings/rules schema、默认规则、presets | `references/configuration.md`、`references/rules.md` | 只修通知实现 bug |
| 修改 Windows toast、sound、popup、custom_command | `references/notifications.md` | 只改规则匹配或 marketplace 注册 |
| 发布、版本、marketplace 注册、验证 | `references/release.md` | 只是本地实验或解释代码 |

## 验证标准

- 修改 Python runtime 后，至少手动调用相关 hook 脚本验证 stdout 是合法 JSON。
- 修改 JSON 后，验证 JSON 可解析。
- 修改 marketplace 注册或插件元数据后，在 marketplace 根目录运行 `claude plugin validate .`。
