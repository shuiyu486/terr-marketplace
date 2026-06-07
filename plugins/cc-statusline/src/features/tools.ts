import type { ToolCompletedCounts, ToolEvent, Config, TranscriptMessage } from "../types";
import { color } from "../colors";

const MAX_TOOLS = 20;
const MAX_RUNNING_SHOWN = 2;
export const TOOL_SEPARATOR = "  │  ";

function getTarget(name: string, input?: Record<string, unknown>): string {
  if (!input) return "";
  switch (name) {
    case "Read":
    case "Write":
    case "Edit":
      return (input.file_path as string) ?? (input.path as string) ?? "";
    case "Grep":
    case "Glob":
      return (input.pattern as string) ?? "";
    case "Bash":
      return ((input.command as string) ?? "").slice(0, 30);
    default:
      return JSON.stringify(input).slice(0, 30);
  }
}

function displayToolName(name: string): string {
  if (!name.startsWith("mcp__")) return name;
  const parts = name.split("__");
  if (parts.length < 3) return name;

  const server = parts[1];
  const rawTool = parts.slice(2).join("__");
  const tool = rawTool.startsWith(`${server}_`) ? rawTool.slice(server.length + 1) : rawTool;
  return `${server}:${tool}`;
}

function incrementCompletedCount(counts: ToolCompletedCounts, name: string): void {
  counts[name] = (counts[name] ?? 0) + 1;
}

function completedCountsFromEvents(events: ToolEvent[]): ToolCompletedCounts {
  const counts: ToolCompletedCounts = {};
  for (const t of events) {
    if (t.status !== "completed") continue;
    incrementCompletedCount(counts, t.name);
  }
  return counts;
}

export function extractToolEvent(
  events: ToolEvent[],
  msg: TranscriptMessage,
  completedCounts?: ToolCompletedCounts,
): void {
  const content = msg?.message?.content;
  if (!Array.isArray(content)) return;

  for (const block of content) {
    if (block.type === "tool_use" && block.id && block.name) {
      const idx = events.findIndex((e) => e.id === block.id);
      if (idx === -1) {
        events.unshift({
          id: block.id,
          name: block.name,
          target: getTarget(block.name, block.input),
          status: "running",
          seenAt: Date.now(),
        });
        if (events.length > MAX_TOOLS) events.length = MAX_TOOLS;
      }
    }

    if (block.type === "tool_result" && block.tool_use_id) {
      const ev = events.find((e) => e.id === block.tool_use_id);
      if (ev && ev.status !== "completed") {
        ev.status = "completed";
        if (completedCounts) incrementCompletedCount(completedCounts, ev.name);
      }
    }
  }
}

export function renderToolParts(
  events: ToolEvent[],
  cfg: Config,
  completedCounts?: ToolCompletedCounts,
): string[] {
  if (!cfg.showToolActivity) return [];

  const parts: string[] = [];

  if (cfg.showRunningTools) {
    const running = events.filter((e) => e.status === "running");
    for (let i = 0; i < Math.min(running.length, MAX_RUNNING_SHOWN); i++) {
      const t = running[i];
      parts.push(`${color("◐", 108)} ${color(displayToolName(t.name), 117)}${t.target ? ` ${color(t.target, 252)}` : ""}`);
    }
  }

  if (cfg.showCompletedTools) {
    const counts = completedCounts ?? completedCountsFromEvents(events);
    const sorted = Object.entries(counts)
      .filter(([, count]) => count > 0)
      .sort((a, b) => b[1] - a[1]);

    for (const [name, count] of sorted) {
      parts.push(`${color("✓", 108)} ${color(displayToolName(name), 117)} ${color(`×${count}`, 244)}`);
    }
  }

  return parts;
}

export function renderTools(
  events: ToolEvent[],
  cfg: Config,
  completedCounts?: ToolCompletedCounts,
): string | null {
  const parts = renderToolParts(events, cfg, completedCounts);
  return parts.length > 0 ? parts.join(TOOL_SEPARATOR) : null;
}
