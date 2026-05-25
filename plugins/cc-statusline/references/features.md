# Features 模块

修改 `src/features/*.ts` 或新增状态栏功能时阅读本文件。

## 统一模式

| 类型 | 职责 |
|------|------|
| `extractXxx(state, msg)` | 从单条 JSONL message 提取事件，可变更新 state |
| `renderXxx(state, cfg)` | 返回 ANSI 字符串片段；无数据返回 `null` |
| service 型 feature | 不渲染行，向主流程补齐数据，例如 `codexLimits.ts` |

`extract*` 由 `transcript.ts` parse 循环调用，且必须在 token 去重前执行。`render*` 由 `render.ts` 按配置条件调用。

## Tool Activity (`features/tools.ts`)

- 数据源：assistant content 中的 `tool_use` 和 `tool_result`
- `tool_use` 创建 running；`tool_result` 标记 completed
- target 提取：Read/Write/Edit→`file_path`，Grep/Glob→`pattern`，Bash→`command[0:30]`，其它→input JSON 摘要
- 按 `tool_use_id` 去重，保留最近 20 条
- 渲染受 `showToolActivity`、`showRunningTools`、`showCompletedTools` 控制

示例：`◐ Edit: auth.ts │ ✓ Read ×3 │ ✓ Grep ×2`

## Agent Tracking (`features/agents.ts`)

- 数据源：`tool_use` name 为 `Task` 或 `Agent`，以及对应 `tool_result`
- 字段：`subagent_type`、`model`、`description`、`startTime`、可选 `endTime`
- 按 `tool_use_id` 去重，保留最近 10 条
- `agentDisplayMode: "compact"` 默认单行摘要：最近 running 明细 + completed 按 agent 类型聚合
- `agentDisplayMode: "multiline"` 多行展开最近保留的全部 agent，并在类型后显示 model
- 展示时 `feature-dev:code-reviewer` 会缩短为 `code-reviewer`

compact 示例：`◷ code-reviewer: 审查正确性 2m │ ✓ code-reviewer ×2 │ ✓ code-explorer ×1`

multiline 示例：
```text
agent: 3 tracked
       ├─ ◷ code-reviewer(sonnet): 审查正确性 2m 15s
       ├─ ✓ code-reviewer(sonnet): 审查项目惯例
       └─ ✓ code-explorer(sonnet): 分析渲染路径
```

## Todo Progress (`features/todos.ts`)

- 数据源：`TodoWrite`、`TaskCreate`、`TaskUpdate`
- `TodoWrite` 完全替换 todo 列表
- `TaskCreate` 追加条目
- `TaskUpdate` 按 id 更新状态
- 状态规范化：`in_progress/running → in_progress`，`completed/complete/done → completed`
- 渲染第一个 in_progress；全部完成时显示完成态

示例：`▸ Fix authentication bug (2/5)`

## Usage Limits Render (`features/limits.ts`)

- 数据源：最终传入 render 的 `data.rate_limits`
- 无 extract 阶段，只负责渲染 usage 行
- 支持 five_hour，存在 seven_day 时一起显示
- 颜色阈值：<75% 绿，75–89% 黄，≥90% 红+粗体

## Codex Limits Fallback (`features/codexLimits.ts`)

这是 service 型 feature，不直接渲染。它在 stdin 缺少 `rate_limits` 时，尝试从本地代理返回的 `X-Codex-*` headers 构造 `rate_limits`。

关键约束：
- 只允许本地代理 URL，避免对任意远程端点发探测请求。
- `codexProbeIntervalMinutes` 控制探测间隔，运行时限制在 1–10 分钟。
- `inflight` promise 必须复用，避免多帧并发探测。
- 首次可等待最多 3000ms；已有缓存时先显示 snapshot。
- 缓存最长可兜底 24 小时。

## 添加新功能

1. 新增 `src/features/<name>.ts`
2. 如需解析 transcript，导出 `extract<Name>` 并在 `transcript.ts` token 去重前调用
3. 如需渲染，导出 `render<Name>` 并在 `render.ts` 按配置调用
4. 必要时扩展 `types.ts` 的 `ParseResult` / `SessionCacheV2` / `Config`
5. 同步 `references/features.md`，涉及配置或渲染时同步对应 reference
