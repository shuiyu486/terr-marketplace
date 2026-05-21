import type { Config, StatusLineData } from "../types";
import { color } from "../colors";

export function renderLimits(
  rateLimits: StatusLineData["rate_limits"],
  cfg: Config,
): string | null {
  if (!cfg.showUsageLimits || !rateLimits?.five_hour) return null;

  const fiveHour = renderWindow("5h", rateLimits.five_hour);
  const sevenDay = rateLimits.seven_day ? renderWindow("7d", rateLimits.seven_day) : null;
  return `${color("usage", 172)}: ${[fiveHour, sevenDay].filter(Boolean).join(" │ ")}`;
}

type LimitWindow = NonNullable<NonNullable<StatusLineData["rate_limits"]>["five_hour"]>;

function renderWindow(
  label: string,
  limit: LimitWindow,
): string {
  const pct = Math.round(limit.used_percentage);
  const filled = Math.max(0, Math.min(10, Math.round(pct / 10)));
  const empty = 10 - filled;

  const barColor = pct >= 90 ? 167 : pct >= 75 ? 215 : 108;
  const bar = color("█".repeat(filled), barColor) + color("░".repeat(empty), 244);

  let resetStr = "";
  if (limit.resets_at) {
    const resetMs = typeof limit.resets_at === "number"
      ? limit.resets_at * 1000
      : new Date(limit.resets_at).getTime();
    const diff = resetMs - Date.now();
    if (Number.isFinite(diff) && diff > 0) {
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff % 86400000) / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const reset = d > 0 ? `${d}d ${h}h` : h > 0 ? `${h}h ${m}m` : `${m}m`;
      resetStr = ` ${color(`(${reset})`, 244)}`;
    }
  }

  const pctStr = color(
    `${pct}%`,
    pct >= 90 ? 167 : pct >= 75 ? 215 : 108,
    pct >= 75,
  );

  return `${color(label, 244)} ${bar} ${pctStr}${resetStr}`;
}
