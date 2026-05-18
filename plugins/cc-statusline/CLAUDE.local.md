## cc-statusline 插件

Claude Code 状态栏插件。每 ~300ms 通过 stdin JSON 读入 `StatusLineData`，解析 transcript JSONL，渲染 ANSI 状态栏。
项目路径在：~\.claude\plugins\marketplaces\terr-marketplace\plugins\cc-statusline

## 模块索引

修改代码时按需读取对应参考文件：

| 修改目标 | 先读参考文件 |
|---------|-------------|
| `src/transcript.ts` | `references/architecture.md` (数据流+缓存) |
| `src/render.ts` | `references/rendering.md` (行格式+颜色) |
| `src/features/*.ts` | `references/features.md` (提取+渲染模式) |
| 配置相关 | `references/config.md` (字段+默认值) |
| 发布 | `references/publish.md` (发布流程) |

## 命令

```bash
npm install && npm run build   # 编译
npm run dev                    # 监听编译
echo '{...}' | node dist/index.js  # 手动测试（见 references/architecture.md 末尾测试用例）
```

## 关键 Gotchas

1. **特性提取顺序**: `extractToolEvent/extractAgentEvent/extractTodoEvent` 必须在 token 去重 `continue` **之前**执行，否则 tool_use/tool_result 事件会丢失（`transcript.ts` 循环中）
2. **colors.ts 独立**: 避免 `render.ts ↔ features/*.ts` 循环依赖
3. **缓存 JSON v2**: 写入 `SessionCacheV2`（`version: 2`），读取兼容旧 CSV 格式
4. **rate_limits 可选**: 有则渲染，无则跳过——不依赖外部快照

## 配置

路径: `~/.claude/cc-statusline.json`。默认全部显示，详见 `references/config.md`。

## 项目结构简图

```
src/
├── index.ts          # 主入口
├── types.ts          # 所有接口
├── transcript.ts     # JSONL 解析 + 缓存 (最复杂)
├── render.ts         # 主渲染入口
├── features/         # 每功能独立 extract+render
├── colors.ts, format.ts, stdin.ts  # 工具
references/           # 按需加载的参考文档
commands/             # setup / configure / update
```

## 代码-文档同步

修改代码后，AI 主动检查并同步更新对应文档：

| 修改代码 | 同步更新文档 |
|---------|-------------|
| `src/transcript.ts` | `references/architecture.md` |
| `src/render.ts` / 颜色 | `references/rendering.md` |
| `src/features/*.ts` | `references/features.md` |
| `Config` 接口 / `DEFAULT_CONFIG` | `references/config.md` |
| `package.json` scripts | `CLAUDE.local.md` 命令 |
| 发布 `.claude-plugin/plugin.json` | `references/publish.md` + `marketplace.json` |
| 发现新 gotcha / bug | `CLAUDE.local.md` Gotchas |

CLAUDE.local.md 本文件存在于两处位置，修改后互相同步。
