## cc-statusline 插件

Claude Code 状态栏插件。每 ~300ms 通过 stdin JSON 读入 `StatusLineData`，解析 transcript JSONL，渲染 ANSI 状态栏。
项目路径在：~\.claude\plugins\marketplaces\terr-marketplace\plugins\cc-statusline

## 模块索引

修改代码时按需读取对应参考文件：

| 修改目标 | 先读参考文件 |
|---------|-------------|
| 理解全项目架构/字段语义 | `references/ai-maintenance.md` (AI 维护手册) |
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
5. **长驻进程 stdin 循环**: `index.ts` 使用 `readStdinLoop()` 长驻模式，进程启动一次循环读 stdin。消除每 ~300ms spawn Node.js 的 Windows Desktop Heap 开销
6. **stdout 即时刷新**: 管道模式下 `process.stdout.write()` 不自动 flush，必须用 `fs.writeSync(1, msg + "\n")` 确保每行即时发送
7. **版本自动迭代**: 任何影响用户功能的变更都必须 bump 版本号（包括 `src/`、`commands/`、`references/`）。bugfix → patch (1.1.1→1.1.2)，feature → minor (1.1.2→1.2.0)。三文件须同步: `package.json`, `.claude-plugin/plugin.json`, `marketplace.json`（在 `.claude-plugin/` 下）。不 bump 则 `cc-statusline:update` 无法识别更新
8. **setup/update 构建检查**: `setup` 在写 settings.json 前检查 `dist/index.js` 是否存在，缺失则自动 `npm install && npm run build`；`update` 版本相同时也检查构建产物，缺失则进入 repair mode 重建
9. **`|| 0` 而非 `?? 0` 防护 NaN**: `input_tokens=0` 的流式中间态行缺少 `cache_creation_input_tokens`/`cache_read_input_tokens` 字段，`0 + undefined = NaN`。`??` 只拦截 null/undefined，`NaN ?? 0` = `NaN`，必须用 `||` 彻底防护。修复后须清理旧缓存避免 NaN 污染链
10. **两个插件目录**: 开发目录 (`marketplaces/.../plugins/cc-statusline`) 和运行时目录 (`cache/.../cc-statusline/{version}`)。`settings.json` 的 `statusLine.command` 指向运行时目录。修改源码后须 `cp dist/` 同步到运行时目录才能生效
11. **ses 与 api 语义不同**: `ses` 按 session 累加（写缓存，同 transcript 内跨 parseTranscript 调用持久），`api` 同 transcript 内持久累加。两者在 `transcript.ts` 中独立累加，共用同一 delta 计算逻辑。新 transcript UUID（Claude Code 重启）→ 新缓存文件 → ses 自然归零。详见 `references/ai-maintenance.md` Line 2 字段详解
12. **缓存按 transcript 路径索引**: `cachePath()` 使用 transcript 文件名（UUID）作为缓存键，而非 Claude PID。同一 transcript 跨重启复用同一缓存，`lineNum` 持久化避免重新解析历史行。旧 PID 键缓存文件（`ses-{pid}.txt`）可安全清理
13. **`os.tmpdir()` 跨环境不一致**: Git Bash 的 `$TEMP` ≠ Node 的 `os.tmpdir()`。缓存实际在 `os.tmpdir()` 返回的路径下

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
| 修改 `src/` 下任何文件 | bump 版本号：`package.json` + `plugin.json` + `marketplace.json` 三文件同步 |
| 修改 `commands/` 下任何文件 | bump 版本号：同上三文件同步 |
| 修改 `references/` 下任何文件 | bump 版本号：同上三文件同步 |
| 字段语义/架构变更 | `references/ai-maintenance.md` |
| 发现新 gotcha / bug | `CLAUDE.local.md` Gotchas |

本文件三处副本须互相同步；marketplaces/ 下的副本为 git 提交入口。
