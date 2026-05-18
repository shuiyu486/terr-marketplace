import type { Config, StatusLineData } from "../types";
import { color } from "../colors";

export function renderLimits(
  rateLimits: StatusLineData["rate_limits"],
  cfg: Config,
): string | null {
  if (!cfg.showUsageLimits || !rateLimits?.five_hour) return null;

  const fh = rateLimits.five_hour;
  const pct = Math.round(fh.used_percentage);
  const filled = Math.round(pct / 10);
  const empty = 10 - filled;

  const barColor = pct >= 90 ? 167 : pct >= 75 ? 215 : 108;
  const bar = color("█".repeat(filled), barColor) + color("░".repeat(empty), 244);

  let resetStr = "";
  if (fh.resets_at) {
    const diff = new Date(fh.resets_at).getTime() - Date.now();
    if (diff > 0) {
      const h = Math.floor(diff / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      resetStr = h > 0 ? ` ${color(`(${h}h ${m}m)`, 244)}` : ` ${color(`(${m}m)`, 244)}`;
    }
  }

  const pctStr = color(
    `${pct}%`,
    pct >= 90 ? 167 : pct >= 75 ? 215 : 108,
    pct >= 75,
  );

  return `${color("usage", 172)}: ${bar} ${pctStr}${resetStr}`;
}
