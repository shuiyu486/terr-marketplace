# 渲染规则

修改 `src/render.ts`、颜色、行格式或 token 显示文案时阅读本文件。

## 行格式

```text
Line 1: model │ effort │ ctx:inTok/ctxSize pct%                          [始终显示]
Line 2: in:inTok out:outTok │ ses:sesIn/sesOut │ api:apiTotal │ ts        [showTokensLine]
Line 3: usage: 5h ███░░░░░░░ 30% (4h 40m) │ 7d █░░░░░░░░░ 5% (5d 12h)    [showUsageLimits, 有数据]
Line 4: tools: ◐ Read file.ts │ ✓ Read ×3                                [showToolActivity]
Line 5: agent: ◷ explore: desc (2m 15s)                                  [showAgentTracking]
Line 6: todo: ▸ Fix bug (2/5)                                             [showTodoProgress]
Line 7: path: /dir                                                        [showPath]
```

每行仅在配置启用且有数据时渲染。

## Line 2 数据来源

| 标签 | 变量 | 来源 | 生命周期 |
|------|------|------|----------|
| `in/out` | `data.context_window.total_*_tokens` | stdin 实时快照 | 实时变化 |
| `ses` | `ctx.sesIn / ctx.sesOut` | transcript 增量解析 + sessionKey cache | 当前 Claude Code session |
| `api` | `ctx.apiIn + ctx.apiOut` | transcript 增量解析 + transcript cache | 当前 transcript 历史累计 |

`ses` 不是单次 parse delta；SessionStart 不变时可跨短生命周期进程恢复。`api` 不按 session 归零。

## Context 兜底

刷新期间 stdin 可能短暂给出 `context_window` 的 `0/0` 帧。渲染层应按 transcript 缓存上一帧有效 context，避免跨进程刷新时显示 `ctx:0/0 0%` 闪烁。

只有 `context_window_size > 0` 且 token/百分比至少一个非零的帧会刷新缓存；坏的零帧不会覆盖最后可信值。

## ANSI 256 色约定

| 场景 | 色号 | 说明 |
|------|------|------|
| context > danger threshold | 168 + bold | 红色危险 |
| context > warn threshold | 215 + bold | 黄色警告 |
| context normal | 108 | 绿色正常 |
| effort max/xhigh/high | 168/167/215 + bold | 高 effort 强调 |
| effort medium/low | 108/115 | 普通 effort |
| model name | 111 | 浅紫 |
| label | 74 | 灰蓝 |
| numeric value | 252 | 浅灰 |
| session value | 115 | |
| api total | 172 | |
| timestamp | 244 | |
| path | 115 | |
| usage filled | 108/215/167 | 按百分比 |
| usage empty | 244 | |
| running icon | 108 | |
| completed icon | 244 | |
| agent type label | 141 | |
| todo icon | 172 | |
| todo subject | 252 | |

## 颜色工具

`src/colors.ts` 独立导出 `color()`、`fg()`、`RESET`、`BOLD`。保持独立是为了避免 `render.ts` 和 `features/*.ts` 循环依赖。

## 数字格式化

`src/format.ts` 的 `fmtW(n)` 负责把 token 数压缩为适合状态栏的短格式；修改格式时同步更新本文件的示例行。
