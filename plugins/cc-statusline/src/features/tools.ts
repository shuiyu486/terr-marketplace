import type { ToolEvent, Config, TranscriptMessage } from "../types";
import { color } from "../colors";

const MAX_TOOLS = 20;
const MAX_RUNNING_SHOWN = 2;
const MAX_COMPLETED_TYPES = 4;

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

export function extractToolEvent(events: ToolEvent[], msg: TranscriptMessage): void {
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
      if (ev) ev.status = "completed";
    }
  }
}

export function renderTools(events: ToolEvent[], cfg: Config): string | null {
  if (!cfg.showToolActivity || events.length === 0) return null;

  const parts: string[] = [];

  if (cfg.showRunningTools) {
    const running = events.filter((e) => e.status === "running");
    for (let i = 0; i < Math.min(running.length, MAX_RUNNING_SHOWN); i++) {
      const t = running[i];
      parts.push(`${color("◐", 108)} ${color(t.name, 117)}${t.target ? ` ${color(t.target, 252)}` : ""}`);
    }
  }

  if (cfg.showCompletedTools) {
    const completed = events.filter((e) => e.status === "completed");
    const counts: Record<string, number> = {};
    for (const t of completed) {
      counts[t.name] = (counts[t.name] ?? 0) + 1;
    }
    const sorted = Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, MAX_COMPLETED_TYPES);

    for (const [name, count] of sorted) {
      parts.push(`${color("✓", 108)} ${color(name, 117)} ${color(`×${count}`, 244)}`);
    }
  }

  return parts.length > 0 ? parts.join("  │  ") : null;
}
