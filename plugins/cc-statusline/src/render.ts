import type { StatusLineData, Config, ParseResult } from "./types";
import { fmtW } from "./format";
import { color } from "./colors";
import { renderTools } from "./features/tools";
import { renderAgents } from "./features/agents";
import { renderTodos } from "./features/todos";
import { renderLimits } from "./features/limits";

function ctxColor(pct: number, cfg: Config): string {
  if (pct > cfg.ctxDangerThreshold) return color(`${pct}%`, 168, true);
  if (pct > cfg.ctxWarnThreshold) return color(`${pct}%`, 215, true);
  return color(`${pct}%`, 108);
}

function effortColor(level: string): string {
  switch (level) {
    case "max": return color(level.toUpperCase(), 168, true);
    case "xhigh": return color(level, 167, true);
    case "high": return color(level, 215, true);
    case "medium": return color(level, 108);
    case "low": return color(level, 115);
    default: return level;
  }
}

function now(): string {
  const d = new Date();
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}:${String(d.getSeconds()).padStart(2, "0")}`;
}

export function render(
  data: StatusLineData,
  ctx: ParseResult,
  cfg: Config,
): string {
  const model = color(data.model.display_name, 111);
  const effort = cfg.showEffort ? ` ${effortColor(data.effort.level)}` : "";
  const pct = Math.round(data.context_window.used_percentage);
  const ctxInfo = ctxColor(pct, cfg);
  const inTok = fmtW(data.context_window.total_input_tokens);
  const ctxSize = fmtW(data.context_window.context_window_size);

  const lines: string[] = [];

  // Line 1: model + effort + context
  const line1 = `${model}${effort} │ ${color("ctx", 74)}:${color(inTok, 252)}/${color(ctxSize, 252)} ${ctxInfo}`;
  lines.push(line1);

  // Line 2: tokens / session / api
  if (cfg.showTokensLine) {
    const outTok = fmtW(data.context_window.total_output_tokens);
    const sesIn = fmtW(ctx.sesApiIn);
    const sesOut = fmtW(ctx.sesApiOut);
    const apiTotal = fmtW(ctx.sesApiIn + ctx.sesApiOut);
    const ts = color(now(), 244);
    const line2 = `${color("in", 74)}:${color(inTok, 252)} ${color("out", 74)}:${color(outTok, 252)} │ ${color("ses", 138)}:${color(sesIn, 115)}/${color(sesOut, 115)} │ ${color("api", 172)}:${color(apiTotal, 172)} │ ${ts}`;
    lines.push(line2);
  }

  // Line 3: usage limits
  const limitLine = renderLimits(data.rate_limits, cfg);
  if (limitLine) lines.push(limitLine);

  // Line 4: tool activity
  const toolLine = renderTools(ctx.tools, cfg);
  if (toolLine) lines.push(`${color("tools", 74)}: ${toolLine}`);

  // Line 5: agent tracking
  const agentLine = renderAgents(ctx.agents, cfg);
  if (agentLine) lines.push(`${color("agent", 141)}: ${agentLine}`);

  // Line 6: todo progress
  const todoLine = renderTodos(
    ctx.todos,
    ctx.todoCompleted,
    ctx.todoTotal,
    cfg,
  );
  if (todoLine) lines.push(`${color("todo", 115)}: ${todoLine}`);

  // Last line: path
  const dir = data.workspace?.current_dir ?? data.cwd;
  if (cfg.showPath && dir) {
    const path = color(dir, 115);
    lines.push(`${color("path", 74)}:${path}`);
  }

  return lines.join("\n");
}
