import { color, RESET } from "./colors";

export const DEFAULT_TERMINAL_COLUMNS = 120;

const ANSI_PATTERN = /\x1b\[[0-9;]*m/g;

type RecordValue = Record<string, unknown>;

export interface WrapAnsiPartsOptions {
  firstLineWidth: number;
  nextLineWidth: number;
  maxLines: number;
  separator: string;
  overflowColor?: number;
}

export function stripAnsi(text: string): string {
  return text.replace(ANSI_PATTERN, "");
}

export function visibleWidth(text: string): number {
  let width = 0;
  for (const char of Array.from(stripAnsi(text))) {
    width += charWidth(char.codePointAt(0) ?? 0);
  }
  return width;
}

export function terminalColumns(source?: unknown, fallback = DEFAULT_TERMINAL_COLUMNS): number {
  const fromSource = columnsFromSource(source);
  if (fromSource) return fromSource;

  const fromStdout = validColumns(process.stdout.columns);
  if (fromStdout) return fromStdout;

  const fromStderr = validColumns(process.stderr.columns);
  if (fromStderr) return fromStderr;

  const fromEnv = validColumns(process.env.COLUMNS);
  return fromEnv ?? fallback;
}

export function wrapAnsiParts(parts: string[], options: WrapAnsiPartsOptions): string[] {
  if (parts.length === 0 || options.maxLines <= 0) return [];

  const separator = options.separator;
  const overflowColor = options.overflowColor ?? 244;
  const maxLines = Math.max(1, options.maxLines);
  const widths = Array.from({ length: maxLines }, (_, index) =>
    Math.max(1, index === 0 ? options.firstLineWidth : options.nextLineWidth)
  );
  const rows: string[][] = [[]];
  let shown = 0;
  let index = 0;

  while (index < parts.length) {
    const rowIndex = rows.length - 1;
    const row = rows[rowIndex];
    const width = widths[rowIndex];
    const part = parts[index];
    const candidate = joinParts([...row, part], separator);

    if (visibleWidth(candidate) <= width) {
      row.push(part);
      shown++;
      index++;
      continue;
    }

    if (row.length === 0) {
      row.push(truncateAnsi(part, width, color("…", overflowColor)));
      shown++;
      index++;
      continue;
    }

    if (rows.length < maxLines) {
      rows.push([]);
      continue;
    }

    break;
  }

  const hidden = parts.length - shown;
  if (hidden > 0) {
    const lastRowIndex = rows.length - 1;
    rows[lastRowIndex] = appendOverflow(rows[lastRowIndex], hidden, widths[lastRowIndex], separator, overflowColor);
  }

  return rows.map((row) => joinParts(row, separator)).filter(Boolean);
}

function columnsFromSource(source: unknown): number | null {
  if (!isRecord(source)) return null;

  const terminal = source.terminal;
  if (isRecord(terminal)) {
    const terminalColumns = validColumns(terminal.columns) ?? validColumns(terminal.width);
    if (terminalColumns) return terminalColumns;
  }

  return (
    validColumns(source.terminal_columns) ??
    validColumns(source.terminalColumns) ??
    validColumns(source.columns) ??
    validColumns(source.width)
  );
}

function validColumns(value: unknown): number | null {
  const n = Number(value);
  if (!Number.isFinite(n)) return null;
  const columns = Math.floor(n);
  return columns >= 1 && columns <= 500 ? columns : null;
}

function isRecord(value: unknown): value is RecordValue {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function charWidth(codePoint: number): number {
  if (codePoint === 0) return 0;
  if (codePoint < 32 || (codePoint >= 0x7f && codePoint < 0xa0)) return 0;
  if (isCombining(codePoint)) return 0;
  return isWide(codePoint) ? 2 : 1;
}

function isCombining(codePoint: number): boolean {
  return (
    (codePoint >= 0x0300 && codePoint <= 0x036f) ||
    (codePoint >= 0x1ab0 && codePoint <= 0x1aff) ||
    (codePoint >= 0x1dc0 && codePoint <= 0x1dff) ||
    (codePoint >= 0x20d0 && codePoint <= 0x20ff) ||
    (codePoint >= 0xfe20 && codePoint <= 0xfe2f)
  );
}

function isWide(codePoint: number): boolean {
  return codePoint >= 0x1100 && (
    codePoint <= 0x115f ||
    codePoint === 0x2329 ||
    codePoint === 0x232a ||
    (codePoint >= 0x2e80 && codePoint <= 0xa4cf && codePoint !== 0x303f) ||
    (codePoint >= 0xac00 && codePoint <= 0xd7a3) ||
    (codePoint >= 0xf900 && codePoint <= 0xfaff) ||
    (codePoint >= 0xfe10 && codePoint <= 0xfe19) ||
    (codePoint >= 0xfe30 && codePoint <= 0xfe6f) ||
    (codePoint >= 0xff00 && codePoint <= 0xff60) ||
    (codePoint >= 0xffe0 && codePoint <= 0xffe6) ||
    (codePoint >= 0x1f300 && codePoint <= 0x1f64f) ||
    (codePoint >= 0x1f900 && codePoint <= 0x1f9ff) ||
    (codePoint >= 0x20000 && codePoint <= 0x3fffd)
  );
}

function joinParts(parts: string[], separator: string): string {
  return parts.join(separator);
}

function appendOverflow(
  row: string[],
  hiddenCount: number,
  width: number,
  separator: string,
  overflowColor: number,
): string[] {
  const kept = [...row];
  let hidden = hiddenCount;

  while (true) {
    const marker = color(`… +${hidden}`, overflowColor);
    const candidate = joinParts(kept.length > 0 ? [...kept, marker] : [marker], separator);
    if (visibleWidth(candidate) <= width) return kept.length > 0 ? [...kept, marker] : [marker];

    if (kept.length === 0) {
      const ellipsis = color("…", overflowColor);
      return [visibleWidth(ellipsis) <= width ? ellipsis : truncateAnsi(ellipsis, width, "")];
    }
    kept.pop();
    hidden++;
  }
}

function truncateAnsi(text: string, maxWidth: number, suffix: string): string {
  if (maxWidth <= 0) return "";
  if (visibleWidth(text) <= maxWidth) return text;

  const suffixWidth = visibleWidth(suffix);
  if (suffixWidth >= maxWidth) return takeAnsiWidth(suffix, maxWidth) + RESET;

  return takeAnsiWidth(text, maxWidth - suffixWidth) + suffix + RESET;
}

function takeAnsiWidth(text: string, maxWidth: number): string {
  let result = "";
  let width = 0;

  for (let i = 0; i < text.length;) {
    if (text[i] === "\x1b" && text[i + 1] === "[") {
      const end = text.indexOf("m", i + 2);
      if (end !== -1) {
        result += text.slice(i, end + 1);
        i = end + 1;
        continue;
      }
    }

    const codePoint = text.codePointAt(i);
    if (codePoint === undefined) break;
    const char = String.fromCodePoint(codePoint);
    const charDisplayWidth = charWidth(codePoint);
    if (width + charDisplayWidth > maxWidth) break;

    result += char;
    width += charDisplayWidth;
    i += char.length;
  }

  return result;
}
