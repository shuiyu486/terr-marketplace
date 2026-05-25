import type { AgentEvent, Config, TranscriptMessage } from "../types";
import { color } from "../colors";

const MAX_AGENTS = 10;
const MAX_COMPACT_RUNNING = 1;
const MAX_COMPACT_COMPLETED = 2;
const MAX_DESCRIPTION_LENGTH = 500;

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

      const desc = normalizeDescription(
        block.input?.description ?? block.input?.task ?? block.input?.prompt ?? ""
      );

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
      if (agent && agent.status !== "completed") {
        agent.status = "completed";
        agent.endTime = Date.now();
      }
    }
  }
}

function normalizeDescription(value: unknown): string {
  return String(value).replace(/\s+/g, " ").trim().slice(0, MAX_DESCRIPTION_LENGTH);
}

function displayType(type: string): string {
  const parts = type.split(":").filter(Boolean);
  return parts.length > 0 ? parts[parts.length - 1] : type;
}

function typeLabel(agent: AgentEvent, showModel: boolean): string {
  const type = displayType(agent.type);
  return showModel && agent.model ? `${type}(${agent.model})` : type;
}

function formatDuration(startTime: number, endTime: number, compact: boolean): string {
  const seconds = Math.max(0, Math.round((endTime - startTime) / 1000));
  if (seconds < 60) return `${seconds}s`;

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    if (compact) return `${minutes}m`;
    const remainder = seconds % 60;
    return remainder === 0 ? `${minutes}m` : `${minutes}m ${remainder}s`;
  }

  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  return compact || remainder === 0 ? `${hours}h` : `${hours}h ${remainder}m`;
}

function agentElapsed(agent: AgentEvent, compact: boolean): string {
  return formatDuration(agent.startTime, agent.endTime ?? Date.now(), compact);
}

function renderRunningAgent(agent: AgentEvent): string {
  return `${color("◷", 108)} ${color(typeLabel(agent, false), 141)}: ${color(agent.description, 252)} ${color(agentElapsed(agent, true), 244)}`;
}

function renderAgentsCompact(agents: AgentEvent[]): string | null {
  const parts: string[] = [];
  const running = agents.filter((a) => a.status === "running").slice(0, MAX_COMPACT_RUNNING);

  for (const agent of running) {
    parts.push(renderRunningAgent(agent));
  }

  const completedCounts = new Map<string, number>();
  for (const agent of agents) {
    if (agent.status !== "completed") continue;
    const type = displayType(agent.type);
    completedCounts.set(type, (completedCounts.get(type) ?? 0) + 1);
  }

  for (const [type, count] of Array.from(completedCounts).slice(0, MAX_COMPACT_COMPLETED)) {
    parts.push(`${color("✓", 108)} ${color(type, 141)} ${color(`×${count}`, 244)}`);
  }

  return parts.length > 0 ? parts.join("  │  ") : null;
}

function renderAgentMultiline(agent: AgentEvent, isLast: boolean): string {
  const branch = isLast ? "└─" : "├─";
  const icon = agent.status === "running" ? "◷" : "✓";
  const iconColor = agent.status === "running" ? 108 : 244;
  const elapsed = agent.status === "running" || agent.endTime
    ? ` ${color(agentElapsed(agent, false), 244)}`
    : "";

  return `${branch} ${color(icon, iconColor)} ${color(typeLabel(agent, true), 141)}: ${color(agent.description, 252)}${elapsed}`;
}

function renderAgentsMultiline(agents: AgentEvent[]): string {
  const lines = [color(`${agents.length} tracked`, 244)];
  agents.forEach((agent, index) => {
    lines.push(renderAgentMultiline(agent, index === agents.length - 1));
  });
  return lines.join("\n");
}

export function renderAgents(agents: AgentEvent[], cfg: Config): string | null {
  if (!cfg.showAgentTracking || agents.length === 0) return null;
  if (cfg.agentDisplayMode === "multiline") return renderAgentsMultiline(agents);
  return renderAgentsCompact(agents);
}
