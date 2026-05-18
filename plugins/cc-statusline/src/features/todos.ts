import type { TodoItem, Config, TranscriptMessage } from "../types";
import { color } from "../colors";

export interface TodoState {
  items: TodoItem[];
  completed: number;
  total: number;
}

export function extractTodoEvent(state: TodoState, msg: TranscriptMessage): void {
  const content = msg?.message?.content;
  if (!Array.isArray(content)) return;

  for (const block of content) {
    if (block.type !== "tool_use" || !block.name) continue;

    switch (block.name) {
      case "TodoWrite": {
        const todos = block.input?.todos ?? block.input?.items;
        if (!Array.isArray(todos)) break;
        state.items = todos.map((t: any) => ({
          id: String(t.id ?? ""),
          subject: String(t.subject ?? t.description ?? t.title ?? "").slice(0, 40),
          status: normalizeStatus(t.status),
        }));
        state.completed = state.items.filter(
          (t) => t.status === "completed"
        ).length;
        state.total = state.items.length;
        break;
      }

      case "TaskCreate": {
        const found = state.items.find(
          (t) => t.id === String(block.input?.taskId ?? "")
        );
        if (!found) {
          state.items.push({
            id: String(block.input?.taskId ?? ""),
            subject: String(
              block.input?.subject ?? block.input?.description ?? ""
            ).slice(0, 40),
            status: normalizeStatus(block.input?.status),
          });
          state.total = state.items.length;
          if (normalizeStatus(block.input?.status) === "completed") {
            state.completed++;
          }
        }
        break;
      }

      case "TaskUpdate": {
        const target = state.items.find(
          (t) => t.id === String(block.input?.taskId ?? "")
        );
        if (target) {
          const old = target.status;
          target.status = normalizeStatus(
            block.input?.status ?? block.input?.state
          );
          if (block.input?.subject) {
            target.subject = String(block.input.subject).slice(0, 40);
          }
          if (old !== "completed" && target.status === "completed") {
            state.completed++;
          } else if (old === "completed" && target.status !== "completed") {
            state.completed = Math.max(0, state.completed - 1);
          }
        }
        break;
      }
    }
  }
}

function normalizeStatus(s: any): string {
  const v = String(s ?? "pending").toLowerCase();
  if (v === "in_progress" || v === "running") return "in_progress";
  if (v === "completed" || v === "complete" || v === "done") return "completed";
  if (v === "skipped" || v === "cancelled") return "skipped";
  return "pending";
}

export function renderTodos(
  items: TodoItem[],
  completed: number,
  total: number,
  cfg: Config,
): string | null {
  if (!cfg.showTodoProgress || total === 0) return null;

  const inProgress = items.find((t) => t.status === "in_progress");

  if (!inProgress) {
    if (completed === total && total > 0) {
      return color(`✓ All tasks complete (${completed}/${total})`, 108);
    }
    return null;
  }

  return `${color("▸", 172)} ${color(inProgress.subject, 252)} ${color(`(${completed}/${total})`, 244)}`;
}
