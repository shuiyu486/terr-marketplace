# Features 模块

修改 `src/features/*.ts` 时阅读本文件。每个功能遵循统一模式：`extract*` 提取 + `render*` 渲染。

## 统一模式

| 导出 | 职责 |
|------|------|
| `extractXxx(state, msg)` | 从一条 JSONL message 提取事件，可变更新 state |
| `renderXxx(state, cfg)` | 返回 ANSI 字符串片段，无数据返回 `null` |

`extract` 函数由 `transcript.ts` 的 parse 循环调用（在 token 去重之前）。`render` 函数由 `render.ts` 条件调用。

## Tool Activity (`features/tools.ts`)

- **数据源**: JSONL 中 `tool_use` (type=assistant) + `tool_result` 块
- **提取**: tool_use → 创建 "running" ToolEvent；tool_result → 标记 "completed"
- **Target 提取**: Read/Write/Edit→file_path, Grep/Glob→pattern, Bash→command[0:30], 其他→input JSON[0:30]
- **去重**: 按 tool_use_id
- **限制**: 保留最近 20 条
- **渲染**: 由 `showToolActivity`(总开关) / `showRunningTools` / `showCompletedTools` 控制。最多 2 个 running (◐), 最多 4 种 completed 类型 (✓ name ×count)。运行中和已完成可独立开关。
- **示例**: `◐ Edit: auth.ts  │  ✓ Read ×3  │  ✓ Grep ×2`

## Agent Tracking (`features/agents.ts`)

- **数据源**: JSONL 中 `tool_use` name="Task"|"Agent" + tool_result
- **提取**: tool_use → "running" AgentEvent；tool_result → "completed"
- **字段**: subagent_type, model, description[0:40], startTime
- **去重**: 按 tool_use_id
- **限制**: 保留最近 10 条
- **渲染**: 最多 3 条 (mix running+completed)，elapsed 格式 `Xm Ys`
- **示例**: `◷ explore: Finding auth code (2m 15s)`

## Todo Progress (`features/todos.ts`)

- **数据源**: JSONL 中 `tool_use` name="TodoWrite"|"TaskCreate"|"TaskUpdate"
- **TodoWrite**: 完全替换 todo 列表
- **TaskCreate**: 追加新条目
- **TaskUpdate**: 更新 status（支持 id 匹配）
- **状态规范化**: in_progress/running→in_progress, completed/complete/done→completed
- **渲染**: 第一个 in_progress 的 "▸ subject (completed/total)"；全部完成时 "✓ All tasks complete"
- **示例**: `▸ Fix authentication bug (2/5)`

## Usage Limits (`features/limits.ts`)

- **数据源**: 优先使用 stdin JSON `rate_limits.five_hour`；本地代理环境下 `features/codexLimits.ts` 会按 `codexProbeIntervalMinutes`（默认 3 分钟，范围 1-10）定时探测 `X-Codex-*` headers 并缓存，缓存最长可兜底显示 24 小时，避免刷新前或短暂探测失败时整行消失
- **无 transcript 提取阶段** — stdin/headers 转换后渲染
- **渲染**: 同一行显示 5h 与可选 7d 窗口；每个窗口包含 10 字符进度条 (█ 已用 / ░ 剩余) + 百分比 + 重置倒计时
- **颜色**: <75% 绿(108), 75-89% 黄(215), ≥90% 红(167)+粗
- **示例**: `usage: 5h ███░░░░░░░ 30% (4h 40m) │ 7d █░░░░░░░░░ 5% (5d 12h)`

## 添加新功能

1. 创建 `src/features/new-feature.ts`
2. 导出 `extractNewFeature(state, msg)` + `renderNewFeature(state, cfg)`
3. 在 `transcript.ts` 的 parse 循环中调用 extract
4. 在 `render.ts` 中添加条件渲染
5. 在 `types.ts` 扩展 `ParseResult` / `SessionCacheV2`
6. 在 `index.ts` 的 `DEFAULT_CONFIG` 添加开关
7. 更新 `references/features.md` 和 `references/config.md`
