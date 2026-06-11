# CLAUDE.local.md — hook-terr 插件维护入口

本目录用于维护 `hook-terr`，一个可扩展的 Claude Code hook runtime 插件。

## 重要原则

- `hook-terr` 是 `shuiyu486/terr-marketplace` 中的 Claude Code 插件，源码、默认配置、presets 和文档都通过 `terr-marketplace` 分发。
- 修改 hook 协议、规则 schema、通知命令或 marketplace 注册前，按下方路由读取对应 reference。
- 只读取当前任务命中的 reference 文件；不要预读整套 references。



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
