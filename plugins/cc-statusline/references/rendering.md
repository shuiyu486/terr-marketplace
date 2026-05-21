# 渲染规则

修改 `src/render.ts` 或颜色相关逻辑时阅读本文件。

## 行格式

```
Line 1: model │ effort │ ctx:inTok/ctxSize pct%        [始终显示]
Line 2: in:inTok out:outTok │ ses:sesIn/sesOut │ api:apiTotal │ ts  [showTokensLine]
Line 3: usage: 5h ███░░░░░░░ 30% (4h 40m) │ 7d █░░░░░░░░░ 5% (5d 12h)  [showUsageLimits, 有数据时]
Line 4: tools: ◐ Read file.ts  │  ✓ Read ×3           [showToolActivity, showRunningTools/showCompletedTools]
Line 5: agent: ◷ explore: desc (2m 15s)               [showAgentTracking]
Line 6: todo: ▸ Fix bug (2/5)                          [showTodoProgress]
Line 7: path: /dir                                     [showPath]
```

每行仅在配置启用 **且** 有数据时渲染。

## Line 2 字段数据来源

```
in:inTok out:outTok │ ses:sesIn/sesOut │ api:apiTotal │ HH:MM:SS
```

| 标签 | 变量 | 数据来源 | 生命周期 |
|------|------|---------|---------|
| in/out | `data.context_window.total_{input,output}_tokens` 经 `stableContextWindow()` 过滤短暂 0 输入帧 | stdin 实时快照 + 进程内 last-known-good | 实时；流式输出期间若收到 0/0 空帧则保持上一帧有效值 |
| ses | `ctx.sesIn / ctx.sesOut` | transcript 增量解析，**不从缓存恢复** | 进程重启归零 |
| api | `ctx.apiIn + ctx.apiOut` | transcript 增量解析，**从缓存恢复** | 跨重启持久

## ANSI 256 色约定

| 场景 | 色号 | 说明 |
|------|------|------|
| context > 90% | 168 + 粗体 | 红（危险） |
| context > 70% | 215 + 粗体 | 黄（警告） |
| context else | 108 | 绿（正常） |
| effort max | 168 + 粗体 | |
| effort xhigh | 167 + 粗体 | |
| effort high | 215 + 粗体 | |
| effort medium | 108 | |
| effort low | 115 | |
| model name | 111 | 浅紫 |
| label (in/out/ctx/etc) | 74 | 灰蓝 |
| numeric value | 252 | 浅灰 |
| session label | 138 | |
| session value | 115 | |
| api total | 172 | |
| timestamp | 244 | |
| path | 115 | |
| usage bar filled | 108/215/167 | 按 % |
| usage bar empty | 244 | |
| running icon (◐◷) | 108 | |
| completed icon (✓) | 244 | |
| agent type label | 141 | |
| todo icon (▸) | 172 | |
| todo subject | 252 | |

## 颜色工具 (src/colors.ts)

```typescript
color(text: string, code: number, bold?: boolean): string  // 包装 ANSI 转义
fg(code: number): string    // 仅前景色
RESET: string               // "\x1b[0m"
BOLD: string                // "\x1b[1m"
```

`color()` 内部处理 bold + reset，是最常用的接口。独立模块避免 `render.ts ↔ features/*.ts` 循环依赖。

## 数字格式化 (src/format.ts)

`fmtW(n)`: >=10w→X.XXw, >=1w→X.XXw, >=1k→X.XXw, else→原始数字
