import type { StatusLineData, Config } from "./types";
import { fmtW } from "./format";

const ESC = "\x1b[";
const RESET = `${ESC}0m`;
const BOLD = `${ESC}1m`;

function fg(n: number): string {
  return `${ESC}38;5;${n}m`;
}

function color(text: string, code: number, bold = false): string {
  return `${bold ? BOLD : ""}${fg(code)}${text}${RESET}`;
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

export function render(
  data: StatusLineData,
  sesApiIn: number,
  sesApiOut: number,
  cfg: Config,
): string {
  const model = color(data.model.display_name, 111);
  const effort = cfg.showEffort ? ` ${effortColor(data.effort.level)}` : "";
  const pct = Math.round(data.context_window.used_percentage);
  const ctx = ctxColor(pct, cfg);
  const inTok = fmtW(data.context_window.total_input_tokens);
  const ctxSize = fmtW(data.context_window.context_window_size);

  const line1 = `${model}${effort} │ ${color('ctx', 74)}:${color(inTok, 252)}/${color(ctxSize, 252)} ${ctx}`;

  let lines = line1;

  if (cfg.showTokensLine) {
    const outTok = fmtW(data.context_window.total_output_tokens);
    const sesIn = fmtW(sesApiIn);
    const sesOut = fmtW(sesApiOut);
    const apiTotal = fmtW(sesApiIn + sesApiOut);
    const ts = color(now(), 244);
    const line2 = `${color('in', 74)}:${color(inTok, 252)} ${color('out', 74)}:${color(outTok, 252)} │ ${color('ses', 138)}:${color(sesIn, 115)}/${color(sesOut, 115)} │ ${color('api', 172)}:${color(apiTotal, 172)} │ ${ts}`;
    lines += `\n${line2}`;
  }

  const dir = data.workspace?.current_dir ?? data.cwd;
  if (cfg.showPath && dir) {
    const path = color(dir, 115);
    lines += `\n${color('path', 74)}:${path}`;
  }

  return lines;
}
