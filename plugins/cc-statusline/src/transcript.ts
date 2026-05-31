import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import type { TranscriptMessage, SessionCacheV2, ParseResult, SessionKeySource } from "./types";
import { extractToolEvent } from "./features/tools";
import { extractAgentEvent } from "./features/agents";
import { extractTodoEvent } from "./features/todos";
import type { TodoState } from "./features/todos";

const CACHE_DIR = path.join(os.tmpdir(), "cc-statusline-cache");
const sessionTokenTotals = new Map<string, { sessionKey: string; sesIn: number; sesOut: number }>();

type SessionKeyInfo = {
  key: string;
  source: SessionKeySource;
  sessionId?: string;
};

function parseLine(line: string): TranscriptMessage | null {
  try {
    return JSON.parse(line) as TranscriptMessage;
  } catch {
    return null;
  }
}

function sessionMarker(lines: string[], transcriptPath: string): SessionKeyInfo {
  let sessionStart: string | null = null;

  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i].trim();
    if (!line) continue;
    const msg = parseLine(line);
    if (!msg) continue;

    if (typeof msg.sessionId === "string" && msg.sessionId) {
      return {
        key: `session:${msg.sessionId}`,
        source: "transcript-session-id",
        sessionId: msg.sessionId,
      };
    }

    if (!sessionStart && msg.attachment?.hookEvent === "SessionStart") {
      sessionStart = msg.uuid || msg.timestamp || null;
    }
  }

  if (sessionStart) {
    return { key: `session:${sessionStart}`, source: "session-start" };
  }

  const name = path.basename(transcriptPath, path.extname(transcriptPath));
  return { key: `transcript:${name}`, source: "transcript-uuid-fallback" };
}

function currentSessionKey(lines: string[] | undefined, transcriptPath: string): SessionKeyInfo {
  return lines ? sessionMarker(lines, transcriptPath) : {
    key: `transcript:${path.basename(transcriptPath, path.extname(transcriptPath))}`,
    source: "transcript-uuid-fallback",
  };
}

function ensureCacheDir(): void {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
  }
}

function cachePath(transcriptPath: string): string {
  const name = path.basename(transcriptPath, path.extname(transcriptPath));
  return path.join(CACHE_DIR, `ses-${name}.txt`);
}

function newCacheV2(): SessionCacheV2 {
  return {
    version: 2,
    lineNum: 0,
    lastIn: 0,
    lastOut: 0,
    lastCacheCreate: 0,
    lastCacheRead: 0,
    lastServerToolUseInput: 0,
    sesIn: 0,
    sesOut: 0,
    apiIn: 0,
    apiOut: 0,
    tools: [],
    agents: [],
    todos: [],
    todoCompleted: 0,
    todoTotal: 0,
  };
}

function readCache(transcriptPath: string): SessionCacheV2 {
  const p = cachePath(transcriptPath);
  try {
    const raw = fs.readFileSync(p, "utf8").trim();
    if (!raw) return newCacheV2();

    // Try v2 JSON first
    if (raw.startsWith("{")) {
      const parsed = JSON.parse(raw);
      if (parsed.version === 2) {
        // Migrate old field names
        const cache = parsed as SessionCacheV2;
        if (cache.apiIn === undefined && (parsed as any).sesApiIn !== undefined) {
          cache.apiIn = (parsed as any).sesApiIn || 0;
          cache.apiOut = (parsed as any).sesApiOut || 0;
        }
        return cache;
      }
    }

    // CSV fallback (v1)
    const parts = raw.split(",");
    if (parts.length >= 7) {
      const cache = newCacheV2();
      cache.lineNum = parseInt(parts[0], 10);
      cache.lastIn = parseInt(parts[1], 10);
      cache.lastOut = parseInt(parts[2], 10);
      cache.lastCacheCreate = parseInt(parts[3], 10);
      cache.lastCacheRead = parseInt(parts[4], 10);
      cache.apiIn = parseInt(parts[5], 10);
      cache.apiOut = parseInt(parts[6], 10);
      return cache;
    }
  } catch {
    // Corrupt cache → start fresh
  }
  return newCacheV2();
}

function writeCache(transcriptPath: string, cache: SessionCacheV2): void {
  ensureCacheDir();
  const p = cachePath(transcriptPath);
  fs.writeFileSync(p, JSON.stringify(cache), "utf8");
}

function startLineFromCache(cache: SessionCacheV2, lines: string[]): number {
  const lineNum = cache.lineNum || 0;

  // Legacy caches stored split("\n").length, which includes a trailing empty
  // item. When one JSONL line is appended after that, re-read that boundary.
  if (!cache.sessionKeySource && lineNum > 0) {
    if (lines.length > lineNum && lines[lines.length - 1].trim() === "" && lineNum === lines.length - 1) {
      return lineNum - 1;
    }
    if (lineNum === lines.length && lines[lines.length - 1]?.trim() !== "") {
      return lineNum - 1;
    }
  }

  return Math.max(0, lineNum);
}

function shouldRebuildCache(cache: SessionCacheV2, session: SessionKeyInfo): boolean {
  if (!cache.sessionKey) return session.source === "transcript-session-id";
  return cache.sessionKey !== session.key;
}

function shouldCountForSession(msg: TranscriptMessage, session: SessionKeyInfo): boolean {
  if (session.source !== "transcript-session-id") return true;
  return msg.sessionId === session.sessionId;
}

export function parseTranscript(transcriptPath: string): ParseResult {
  if (!transcriptPath) {
    return {
      sesIn: 0,
      sesOut: 0,
      apiIn: 0,
      apiOut: 0,
      tools: [],
      agents: [],
      todos: [],
      todoCompleted: 0,
      todoTotal: 0,
    };
  }

  const cache = readCache(transcriptPath);

  let lines: string[];

  try {
    const content = fs.readFileSync(transcriptPath, "utf8");
    lines = content.split("\n");
  } catch {
    const session = currentSessionKey(undefined, transcriptPath);
    const sessionTotals = cache.sessionKey === session.key
      ? { sesIn: cache.sesIn || 0, sesOut: cache.sesOut || 0 }
      : { sesIn: 0, sesOut: 0 };
    return {
      sesIn: sessionTotals.sesIn,
      sesOut: sessionTotals.sesOut,
      apiIn: cache.apiIn || 0,
      apiOut: cache.apiOut || 0,
      tools: cache.tools || [],
      agents: cache.agents || [],
      todos: cache.todos || [],
      todoCompleted: cache.todoCompleted || 0,
      todoTotal: cache.todoTotal || 0,
    };
  }

  const session = currentSessionKey(lines, transcriptPath);
  const rebuildCache = shouldRebuildCache(cache, session);
  const startLine = rebuildCache ? 0 : startLineFromCache(cache, lines);
  let maxProcessedLineNum = startLine;

  let apiIn = rebuildCache ? 0 : cache.apiIn || 0;
  let apiOut = rebuildCache ? 0 : cache.apiOut || 0;
  let lastIn = rebuildCache ? 0 : cache.lastIn || 0;
  let lastOut = rebuildCache ? 0 : cache.lastOut || 0;
  let lastCacheCreate = rebuildCache ? 0 : cache.lastCacheCreate || 0;
  let lastCacheRead = rebuildCache ? 0 : cache.lastCacheRead || 0;
  let lastServerToolUseInput = rebuildCache ? 0 : cache.lastServerToolUseInput || 0;

  const tools = rebuildCache ? [] : cache.tools || [];
  const agents = rebuildCache ? [] : cache.agents || [];
  const todoState: TodoState = {
    items: rebuildCache ? [] : cache.todos || [],
    completed: rebuildCache ? 0 : cache.todoCompleted || 0,
    total: rebuildCache ? 0 : cache.todoTotal || 0,
  };

  const memorySessionTotals = rebuildCache ? null : sessionTokenTotals.get(transcriptPath);
  const cachedSessionTotals = !rebuildCache && cache.sessionKey === session.key
    ? { sesIn: cache.sesIn || 0, sesOut: cache.sesOut || 0 }
    : { sesIn: 0, sesOut: 0 };
  const sessionTotals = memorySessionTotals?.sessionKey === session.key
    ? memorySessionTotals
    : cachedSessionTotals;
  let sesIn = sessionTotals.sesIn;
  let sesOut = sessionTotals.sesOut;

  for (let i = startLine; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    const msg = parseLine(line);
    if (!msg) continue;

    // Feature extraction — must run BEFORE token dedup to avoid losing events
    try {
      extractToolEvent(tools, msg);
      extractAgentEvent(agents, msg);
      extractTodoEvent(todoState, msg);
    } catch {
      // Feature extraction errors are non-fatal — skip this message
    }

    maxProcessedLineNum = i + 1;

    // Token accumulation (existing logic)
    if (msg.type === "assistant" && msg.message?.usage) {
      const u = msg.message.usage;
      const serverToolUseInput = u.server_tool_use_input_tokens || 0;
      if (
        u.input_tokens === lastIn &&
        u.output_tokens === lastOut &&
        u.cache_creation_input_tokens === lastCacheCreate &&
        u.cache_read_input_tokens === lastCacheRead &&
        serverToolUseInput === lastServerToolUseInput
      ) {
        continue;
      }

      const deltaIn =
        (u.input_tokens || 0) +
        (u.cache_creation_input_tokens || 0) +
        (u.cache_read_input_tokens || 0) +
        serverToolUseInput;
      const deltaOut = u.output_tokens || 0;

      apiIn += deltaIn;
      apiOut += deltaOut;
      if (shouldCountForSession(msg, session)) {
        sesIn += deltaIn;
        sesOut += deltaOut;
      }

      lastIn = u.input_tokens || 0;
      lastOut = u.output_tokens || 0;
      lastCacheCreate = u.cache_creation_input_tokens || 0;
      lastCacheRead = u.cache_read_input_tokens || 0;
      lastServerToolUseInput = serverToolUseInput;
    }
  }

  // Defensive verification: re-scan transcript for tool_results of stuck
  // running agents. Guards against a race where two concurrent parse instances
  // read the same cache, and the later write overwrites a completed->running
  // transition with a stale "running" value.
  const stuckIds = new Set(
    agents.filter((a) => a.status === "running").map((a) => a.id)
  );
  if (stuckIds.size > 0) {
    for (let i = 0; i < lines.length; i++) {
      const l = lines[i].trim();
      if (!l) continue;
      try {
        const m = JSON.parse(l);
        const c = m?.message?.content;
        if (Array.isArray(c)) {
          for (const block of c) {
            if (block.type === "tool_result" && stuckIds.has(block.tool_use_id)) {
              const agent = agents.find((a) => a.id === block.tool_use_id);
              if (agent) agent.status = "completed";
              stuckIds.delete(block.tool_use_id);
              if (stuckIds.size === 0) break;
            }
          }
        }
      } catch { /* skip malformed JSON lines */ }
      if (stuckIds.size === 0) break;
    }
  }

  sessionTokenTotals.set(transcriptPath, { sessionKey: session.key, sesIn, sesOut });

  const newCache: SessionCacheV2 = {
    version: 2,
    sessionKey: session.key,
    sessionKeySource: session.source,
    lineNum: maxProcessedLineNum,
    lastIn,
    lastOut,
    lastCacheCreate,
    lastCacheRead,
    lastServerToolUseInput,
    sesIn,
    sesOut,
    apiIn,
    apiOut,
    tools,
    agents,
    todos: todoState.items,
    todoCompleted: todoState.completed,
    todoTotal: todoState.total,
  };
  writeCache(transcriptPath, newCache);

  return {
    sesIn,
    sesOut,
    apiIn,
    apiOut,
    tools,
    agents,
    todos: todoState.items,
    todoCompleted: todoState.completed,
    todoTotal: todoState.total,
  };
}
