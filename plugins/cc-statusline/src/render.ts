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
  if (pct > cfg.ctxDangerThreshold) return color(`${pct}%`, 196, true);
  if (pct > cfg.ctxWarnThreshold) return color(`${pct}%`, 220, true);
  return color(`${pct}%`, 82);
}

function effortColor(level: string): string {
  switch (level) {
    case "max": return color(level.toUpperCase(), 201, true);
    case "xhigh": return color(level, 196, true);
    case "high": return color(level, 220, true);
    case "medium": return color(level, 82);
    case "low": return color(level, 117);
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
  const model = color(data.model.display_name, 183);
  const effort = cfg.showEffort ? ` ${effortColor(data.effort.level)}` : "";
  const pct = Math.round(data.context_window.used_percentage);
  const ctx = ctxColor(pct, cfg);
  const inTok = fmtW(data.context_window.total_input_tokens);
  const ctxSize = fmtW(data.context_window.context_window_size);

  const line1 = `${model}${effort} │ ${color('ctx', 147)}:${color(inTok, 183)}/${color(ctxSize, 183)} ${ctx}`;

  let lines = line1;

  if (cfg.showTokensLine) {
    const outTok = fmtW(data.context_window.total_output_tokens);
    const sesIn = fmtW(sesApiIn);
    const sesOut = fmtW(sesApiOut);
    const apiTotal = fmtW(sesApiIn + sesApiOut);
    const ts = color(now(), 245);
    const line2 = `${color('in', 147)}:${color(inTok, 183)} ${color('out', 147)}:${color(outTok, 183)} │ ${color('ses', 109)}:${color(sesIn, 117)}/${color(sesOut, 117)} │ ${color('api', 178)}:${color(apiTotal, 220)} │ ${ts}`;
    lines += `\n${line2}`;
  }

  const dir = data.workspace?.current_dir ?? data.cwd;
  if (cfg.showPath && dir) {
    const path = color(dir, 109);
    lines += `\n${color('path', 109)}:${path}`;
  }

  return lines;
}
