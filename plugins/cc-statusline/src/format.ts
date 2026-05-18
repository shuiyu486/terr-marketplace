export function fmtW(n: number): string {
  if (n >= 100_000) {
    const w = n / 10_000;
    return w % 1 === 0 ? `${w.toFixed(0)}w` : `${w.toFixed(1)}w`;
  }
  if (n >= 10_000) {
    return `${(n / 10_000).toFixed(1)}w`;
  }
  if (n >= 1_000) {
    return `${(n / 10_000).toFixed(2)}w`;
  }
  return String(n);
}
