## cc-statusline 插件

Claude Code 状态栏插件：从 stdin 读取 `StatusLineData`，解析 transcript JSONL，渲染 ANSI 状态栏。

本文件可能存在于开发副本、marketplace 副本或运行时副本；修改任一副本后，同步到其它 cc-statusline 副本，避免会话读取到过期指令。不要在本文件中写死某个副本的绝对路径。

## 按需读取参考

| 修改目标 | 先读参考文件 |
|---------|-------------|
| 全项目架构/字段语义 | `references/ai-maintenance.md` |
| `src/transcript.ts` | `references/architecture.md` |
| `src/render.ts` / 颜色 | `references/rendering.md` |
| `src/features/*.ts` | `references/features.md` |
| 配置相关 | `references/config.md` |
| 发布流程 | `references/publish.md` |

## 常用命令

```bash
npm install && npm run build
npm run dev
echo '{...}' | node dist/index.js
```

手动测试用例见 `references/architecture.md` 末尾。

## 必守 Gotchas

1. `extractToolEvent/extractAgentEvent/extractTodoEvent` 必须在 token 去重 `continue` 前执行，否则 tool 事件会丢失。
2. `colors.ts` 保持独立，避免 `render.ts ↔ features/*.ts` 循环依赖。
3. 缓存写入 `SessionCacheV2`（`version: 2`），按 transcript 文件名/UUID 做缓存键，读取兼容旧 CSV。
4. `rate_limits` 有则渲染；Codex headers fallback 必须复用 in-flight、限制探测频率，并在一次性 stdin 调用结束前等待 pending handler。
5. stdin 使用 `readStdinLoop()` 长驻循环；stdout 用 `fs.writeSync(1, msg + "\n")` 即时刷新。
6. 修改 `src/`、`commands/`、`references/` 或影响用户功能时，按语义化版本同步 bump：`package.json`、`package-lock.json`、`.claude-plugin/plugin.json`、根 `.claude-plugin/marketplace.json`。
7. `ses` 按当前 Claude Code session 累加，`api` 按 transcript 历史持久累加；两者独立，详见 `references/ai-maintenance.md`。
8. `os.tmpdir()` 跨环境可能不同；缓存实际位置以 Node 的 `os.tmpdir()` 为准。

## 配置与同步

用户配置：`${CLAUDE_CONFIG_DIR}/cc-statusline.json`，未设置时为 `~/.claude/cc-statusline.json`；默认全部显示，详见 `references/config.md`。

修改代码后同步相关 reference 文档；发现新 gotcha 时，优先写入对应 reference，只有高频且会影响操作顺序的规则才加入本文件。
