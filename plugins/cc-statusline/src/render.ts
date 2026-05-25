import * as crypto from "crypto";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import type { StatusLineData, Config, ParseResult } from "./types";
import { fmtW } from "./format";
import { color } from "./colors";
import { renderTools } from "./features/tools";
import { renderAgents } from "./features/agents";
import { renderTodos } from "./features/todos";
import { renderLimits } from "./features/limits";

type ContextWindow = StatusLineData["context_window"];

const CACHE_DIR = path.join(os.tmpdir(), "cc-statusline-cache");
let lastContextWindow: ContextWindow | null = null;

function hasContextUsage(current: ContextWindow): boolean {
  return current.context_window_size > 0 && (
    current.total_input_tokens > 0 ||
    current.total_output_tokens > 0 ||
    current.used_percentage > 0
  );
}

function contextCachePath(transcriptPath: string): string | null {
  if (!transcriptPath) return null;
  const name = path.basename(transcriptPath, path.extname(transcriptPath));
  const key = crypto.createHash("sha1").update(path.resolve(transcriptPath)).digest("hex").slice(0, 12);
  return path.join(CACHE_DIR, `ctx-${name}-${key}.json`);
}

function readCachedContextWindow(transcriptPath: string): ContextWindow | null {
  const cachePath = contextCachePath(transcriptPath);
  if (!cachePath) return null;

  try {
    const parsed = JSON.parse(fs.readFileSync(cachePath, "utf8"));
    const value = parsed?.context_window;
    if (value && hasContextUsage(value)) return value as ContextWindow;
  } catch {}

  return null;
}

function writeCachedContextWindow(transcriptPath: string, contextWindow: ContextWindow): void {
  const cachePath = contextCachePath(transcriptPath);
  if (!cachePath) return;

  try {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
    const tmpPath = `${cachePath}.${process.pid}.tmp`;
    fs.writeFileSync(tmpPath, JSON.stringify({ version: 1, context_window: contextWindow }), "utf8");
    fs.renameSync(tmpPath, cachePath);
  } catch {}
}

function stableContextWindow(current: ContextWindow, transcriptPath: string): ContextWindow {
  if (hasContextUsage(current)) {
    lastContextWindow = current;
    writeCachedContextWindow(transcriptPath, current);
    return current;
  }

  return lastContextWindow ?? readCachedContextWindow(transcriptPath) ?? current;
}

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

function pushLabeledLines(lines: string[], label: string, labelColor: number, value: string | null): void {
  if (!value) return;

  const [first, ...rest] = value.split("\n");
  lines.push(`${color(label, labelColor)}: ${first}`);
  const indent = " ".repeat(label.length + 2);
  for (const line of rest) {
    lines.push(`${indent}${line}`);
  }
}

export function render(
  data: StatusLineData,
  ctx: ParseResult,
  cfg: Config,
): string {
  const contextWindow = stableContextWindow(data.context_window, data.transcript_path);
  const model = color(data.model.display_name, 111);
  const effort = cfg.showEffort ? ` ${effortColor(data.effort.level)}` : "";
  const pct = Math.round(contextWindow.used_percentage);
  const ctxInfo = ctxColor(pct, cfg);
  const inTok = fmtW(contextWindow.total_input_tokens);
  const ctxSize = fmtW(contextWindow.context_window_size);

  const lines: string[] = [];

  // Line 1: model + effort + context
  const line1 = `${model}${effort} │ ${color("ctx", 74)}:${color(inTok, 252)}/${color(ctxSize, 252)} ${ctxInfo}`;
  lines.push(line1);

  // Line 2: tokens / session / api
  if (cfg.showTokensLine) {
    const outTok = fmtW(contextWindow.total_output_tokens);
    const sesIn = fmtW(ctx.sesIn);
    const sesOut = fmtW(ctx.sesOut);
    const apiTotal = fmtW(ctx.apiIn + ctx.apiOut);
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
  pushLabeledLines(lines, "agent", 141, renderAgents(ctx.agents, cfg));

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
