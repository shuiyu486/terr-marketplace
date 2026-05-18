## cc-statusline 插件

Claude Code 状态栏插件。每 ~300ms 通过 stdin JSON 读入 `StatusLineData`，解析 transcript JSONL，渲染 ANSI 状态栏。

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

## 同步规则 (长期)

每次修改以下文件后，必须执行同步：

| 文件 | 同步目标 |
|------|---------|
| `CLAUDE.local.md` | `C:\AI\m_projects\cc-statusline\CLAUDE.local.md` |
| `references/*.md` | `C:\AI\m_projects\cc-statusline\references\` |
| `commands/*.md` | `C:\AI\m_projects\cc-statusline\commands\` |
| `src/*.ts` | `.claude-plugin/marketplace.json` 版本号同步 |

同步命令：
```bash
# terr-marketplace → 工作目录
cp ~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/CLAUDE.local.md "C:/AI/m_projects/cc-statusline/"
cp -r ~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/references "C:/AI/m_projects/cc-statusline/"

# 工作目录 → terr-marketplace (反向)
cp "C:/AI/m_projects/cc-statusline/CLAUDE.local.md" ~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/
cp -r "C:/AI/m_projects/cc-statusline/references/"* ~/.claude/plugins/marketplaces/terr-marketplace/plugins/cc-statusline/references/
```

两处文件的 `CLAUDE.local.md` + `references/` + `commands/` 应始终保持一致。
