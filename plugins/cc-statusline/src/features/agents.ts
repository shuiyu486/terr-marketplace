import type { AgentEvent, Config, TranscriptMessage } from "../types";
import { color } from "../colors";

const MAX_AGENTS = 10;
const MAX_SHOWN = 3;

export function extractAgentEvent(agents: AgentEvent[], msg: TranscriptMessage): void {
  const content = msg?.message?.content;
  if (!Array.isArray(content)) return;

  for (const block of content) {
    // Handle tool_use — add "running" agent entries
    if (
      block.type === "tool_use" &&
      block.id &&
      (block.name === "Task" || block.name === "Agent")
    ) {
      const idx = agents.findIndex((a) => a.id === block.id);
      if (idx !== -1) continue;

      const desc = String(
        block.input?.description ?? block.input?.task ?? block.input?.prompt ?? ""
      ).slice(0, 40);

      agents.unshift({
        id: block.id,
        type: (block.input?.subagent_type as string) ?? block.name,
        model: (block.input?.model as string) ?? "",
        description: desc,
        status: "running",
        startTime: Date.now(),
      });

      if (agents.length > MAX_AGENTS) agents.length = MAX_AGENTS;
    }

    // Handle tool_result — mark matching agents as completed
    if (block.type === "tool_result" && block.tool_use_id) {
      const agent = agents.find((a) => a.id === block.tool_use_id);
      if (agent) agent.status = "completed";
    }
  }
}

function formatElapsed(startTime: number): string {
  const s = Math.round((Date.now() - startTime) / 1000);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${m}m ${sec}s`;
}

export function renderAgents(agents: AgentEvent[], cfg: Config): string | null {
  if (!cfg.showAgentTracking || agents.length === 0) return null;

  const shown = agents.slice(0, MAX_SHOWN);
  const parts: string[] = [];

  for (const a of shown) {
    const icon = a.status === "running" ? "◷" : "✓";
    const iconColor = a.status === "running" ? 108 : 244;
    const typeLabel = a.model ? `${a.type}(${a.model})` : a.type;
    const elapsed = a.status === "running" ? ` ${color(formatElapsed(a.startTime), 244)}` : "";

    parts.push(
      `${color(icon, iconColor)} ${color(typeLabel, 141)}: ${color(a.description, 252)}${elapsed}`
    );
  }

  return parts.length > 0 ? parts.join("  │  ") : null;
}
