# 渲染规则

修改 `src/render.ts` 或颜色相关逻辑时阅读本文件。

## 行格式

```
Line 1: model │ effort │ ctx:inTok/ctxSize pct%        [始终显示]
Line 2: tools: ◐ Read file.ts  │  ✓ Read ×3           [showToolActivity]
Line 3: agent: ◷ explore: desc (2m 15s)               [showAgentTracking]
Line 4: todo: ▸ Fix bug (2/5)                          [showTodoProgress]
Line 5: usage: ████████░░ 75% (12h 50m)               [showUsageLimits, 有数据时]
Line 6: in:inTok out:outTok │ ses:in/out │ api:total │ ts  [showTokensLine]
Line 7: path: /dir                                     [showPath]
```

每行仅在配置启用 **且** 有数据时渲染。

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
