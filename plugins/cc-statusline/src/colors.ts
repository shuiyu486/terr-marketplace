export const ESC = "\x1b[";
export const RESET = `${ESC}0m`;
export const BOLD = `${ESC}1m`;

export function fg(n: number): string {
  return `${ESC}38;5;${n}m`;
}

export function color(text: string, code: number, bold = false): string {
  return `${bold ? BOLD : ""}${fg(code)}${text}${RESET}`;
}
