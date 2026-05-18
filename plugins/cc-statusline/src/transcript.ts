import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import * as cp from "child_process";
import type { TranscriptMessage, SessionCache } from "./types";

const CACHE_DIR = path.join(os.tmpdir(), "cc-statusline-cache");

function ensureCacheDir(): void {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
  }
}

function cachePath(pid: number): string {
  return path.join(CACHE_DIR, `ses-${pid}.txt`);
}

function readCache(pid: number): SessionCache | null {
  const p = cachePath(pid);
  try {
    const raw = fs.readFileSync(p, "utf8").trim();
    if (!raw) return null;
    const parts = raw.split(",");
    if (parts.length !== 7) return null;
    return {
      lineNum: parseInt(parts[0], 10),
      lastIn: parseInt(parts[1], 10),
      lastOut: parseInt(parts[2], 10),
      lastCacheCreate: parseInt(parts[3], 10),
      lastCacheRead: parseInt(parts[4], 10),
      sesApiIn: parseInt(parts[5], 10),
      sesApiOut: parseInt(parts[6], 10),
    };
  } catch {
    return null;
  }
}

function writeCache(pid: number, cache: SessionCache): void {
  ensureCacheDir();
  const p = cachePath(pid);
  const line = [
    cache.lineNum,
    cache.lastIn,
    cache.lastOut,
    cache.lastCacheCreate,
    cache.lastCacheRead,
    cache.sesApiIn,
    cache.sesApiOut,
  ].join(",");
  fs.writeFileSync(p, line, "utf8");
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

export function parseTranscript(transcriptPath: string): {
  sesApiIn: number;
  sesApiOut: number;
} {
  if (!transcriptPath) return { sesApiIn: 0, sesApiOut: 0 };

  const pid = findClaudePid();
  const cache = readCache(pid);

  let startLine = cache ? cache.lineNum : 0;
  let sesApiIn = cache ? cache.sesApiIn : 0;
  let sesApiOut = cache ? cache.sesApiOut : 0;
  let lastIn = cache ? cache.lastIn : 0;
  let lastOut = cache ? cache.lastOut : 0;
  let lastCacheCreate = cache ? cache.lastCacheCreate : 0;
  let lastCacheRead = cache ? cache.lastCacheRead : 0;

  let lines: string[];

  try {
    const content = fs.readFileSync(transcriptPath, "utf8");
    lines = content.split("\n");
  } catch {
    return { sesApiIn, sesApiOut };
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

    if (msg.type !== "assistant" || !msg.usage) continue;

    const u = msg.usage;
    // Deduplicate: skip if all 4 token values identical to previous
    if (
      u.input_tokens === lastIn &&
      u.output_tokens === lastOut &&
      u.cache_creation_input_tokens === lastCacheCreate &&
      u.cache_read_input_tokens === lastCacheRead
    ) {
      continue;
    }

    const apiIn =
      u.input_tokens +
      u.cache_creation_input_tokens +
      u.cache_read_input_tokens +
      (u.server_tool_use_input_tokens || 0);
    const apiOut = u.output_tokens;

    sesApiIn += apiIn;
    sesApiOut += apiOut;

    lastIn = u.input_tokens;
    lastOut = u.output_tokens;
    lastCacheCreate = u.cache_creation_input_tokens;
    lastCacheRead = u.cache_read_input_tokens;
  }

  const newCache: SessionCache = {
    lineNum: lines.length,
    lastIn,
    lastOut,
    lastCacheCreate,
    lastCacheRead,
    sesApiIn,
    sesApiOut,
  };
  writeCache(pid, newCache);

  return { sesApiIn, sesApiOut };
}
