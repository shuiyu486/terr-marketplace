import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import * as cp from "child_process";
import type { TranscriptMessage, SessionCacheV2, ParseResult } from "./types";
import { extractToolEvent } from "./features/tools";
import { extractAgentEvent } from "./features/agents";
import { extractTodoEvent } from "./features/todos";
import type { TodoState } from "./features/todos";

const CACHE_DIR = path.join(os.tmpdir(), "cc-statusline-cache");

function ensureCacheDir(): void {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
  }
}

function cachePath(pid: number): string {
  return path.join(CACHE_DIR, `ses-${pid}.txt`);
}

function newCacheV2(): SessionCacheV2 {
  return {
    version: 2,
    lineNum: 0,
    lastIn: 0,
    lastOut: 0,
    lastCacheCreate: 0,
    lastCacheRead: 0,
    apiIn: 0,
    apiOut: 0,
    tools: [],
    agents: [],
    todos: [],
    todoCompleted: 0,
    todoTotal: 0,
  };
}

function readCache(pid: number): SessionCacheV2 {
  const p = cachePath(pid);
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

function writeCache(pid: number, cache: SessionCacheV2): void {
  ensureCacheDir();
  const p = cachePath(pid);
  fs.writeFileSync(p, JSON.stringify(cache), "utf8");
}

function findClaudePid(): number {
  const myPid = process.pid;

  if (process.platform === "win32") {
    try {
      let pid = myPid;
      for (let i = 0; i < 10; i++) {
        const out = cp.execSync(
          `wmic process where "ProcessId=${pid}" get ParentProcessId /value`,
          { encoding: "utf8", timeout: 3000 },
        ).trim();
        const match = out.match(/ParentProcessId=(\d+)/);
        if (!match) break;
        const ppid = parseInt(match[1], 10);
        const name = cp.execSync(
          `wmic process where "ProcessId=${ppid}" get Name /value`,
          { encoding: "utf8", timeout: 3000 },
        ).trim();
        if (/claude/i.test(name)) return ppid;
        pid = ppid;
      }
    } catch {
      // Fall through
    }
  } else {
    try {
      let pid = myPid;
      for (let i = 0; i < 10; i++) {
        const ppid = parseInt(
          cp.execSync(`ps -o ppid= -p ${pid}`, { encoding: "utf8" }).trim(),
          10,
        );
        const name = cp.execSync(`ps -o comm= -p ${ppid}`, {
          encoding: "utf8",
        }).trim();
        if (/claude/i.test(name)) return ppid;
        pid = ppid;
      }
    } catch {
      // Fall through
    }
  }

  return myPid;
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

  const pid = findClaudePid();
  const cache = readCache(pid);

  const startLine = cache.lineNum;
  let apiIn = cache.apiIn || 0;
  let apiOut = cache.apiOut || 0;
  let lastIn = cache.lastIn || 0;
  let lastOut = cache.lastOut || 0;
  let lastCacheCreate = cache.lastCacheCreate || 0;
  let lastCacheRead = cache.lastCacheRead || 0;
  // ses resets every process start
  let sesIn = 0;
  let sesOut = 0;

  const tools = cache.tools;
  const agents = cache.agents;
  const todoState: TodoState = {
    items: cache.todos,
    completed: cache.todoCompleted,
    total: cache.todoTotal,
  };

  let lines: string[];

  try {
    const content = fs.readFileSync(transcriptPath, "utf8");
    lines = content.split("\n");
  } catch {
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

  for (let i = startLine; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    let msg: TranscriptMessage;
    try {
      msg = JSON.parse(line);
    } catch {
      continue;
    }

    // Feature extraction — must run BEFORE token dedup to avoid losing events
    try {
      extractToolEvent(tools, msg);
      extractAgentEvent(agents, msg);
      extractTodoEvent(todoState, msg);
    } catch {
      // Feature extraction errors are non-fatal — skip this message
    }

    // Token accumulation (existing logic)
    if (msg.type === "assistant" && msg.message?.usage) {
      const u = msg.message.usage;
      if (
        u.input_tokens === lastIn &&
        u.output_tokens === lastOut &&
        u.cache_creation_input_tokens === lastCacheCreate &&
        u.cache_read_input_tokens === lastCacheRead
      ) {
        continue;
      }

      const deltaIn =
        (u.input_tokens || 0) +
        (u.cache_creation_input_tokens || 0) +
        (u.cache_read_input_tokens || 0) +
        (u.server_tool_use_input_tokens || 0);
      const deltaOut = u.output_tokens || 0;

      apiIn += deltaIn;
      apiOut += deltaOut;
      sesIn += deltaIn;
      sesOut += deltaOut;

      lastIn = u.input_tokens || 0;
      lastOut = u.output_tokens || 0;
      lastCacheCreate = u.cache_creation_input_tokens || 0;
      lastCacheRead = u.cache_read_input_tokens || 0;
    }
  }

  const newCache: SessionCacheV2 = {
    version: 2,
    lineNum: lines.length,
    lastIn,
    lastOut,
    lastCacheCreate,
    lastCacheRead,
    apiIn,
    apiOut,
    tools,
    agents,
    todos: todoState.items,
    todoCompleted: todoState.completed,
    todoTotal: todoState.total,
  };
  writeCache(pid, newCache);

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
