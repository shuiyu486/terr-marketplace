import type { StatusLineData } from "./types";

const STDIN_TIMEOUT_MS = 500;

/** One-shot read (kept for backward compat / manual testing). */
export async function readStdin(): Promise<StatusLineData | null> {
  if (process.stdin.isTTY) {
    return null;
  }

  return new Promise<StatusLineData | null>((resolve) => {
    let raw = "";
    let settled = false;

    const timer = setTimeout(() => {
      if (!settled) {
        settled = true;
        cleanup();
        resolve(null);
      }
    }, STDIN_TIMEOUT_MS);

    const cleanup = () => {
      clearTimeout(timer);
      process.stdin.removeListener("data", onData);
      process.stdin.removeListener("end", onEnd);
      process.stdin.removeListener("error", onError);
    };

    const onData = (chunk: Buffer | string) => {
      raw += String(chunk);
      const trimmed = raw.trim();
      if (trimmed) {
        try {
          const data = JSON.parse(trimmed) as StatusLineData;
          settled = true;
          cleanup();
          resolve(data);
        } catch {
          // Incomplete JSON, keep reading
        }
      }
    };

    const onEnd = () => {
      if (settled) return;
      settled = true;
      cleanup();
      const trimmed = raw.trim();
      if (!trimmed) {
        resolve(null);
        return;
      }
      try {
        resolve(JSON.parse(trimmed) as StatusLineData);
      } catch {
        resolve(null);
      }
    };

    const onError = () => {
      if (settled) return;
      settled = true;
      cleanup();
      resolve(null);
    };

    process.stdin.setEncoding("utf8");
    process.stdin.on("data", onData);
    process.stdin.on("end", onEnd);
    process.stdin.on("error", onError);
  });
}

/**
 * Long-running stdin loop.
 *
 * Reads complete JSON objects from stdin (each delimited by its own
 * balanced braces) and calls `handler` for each.  Stays alive until
 * stdin ends or errors — the single Node.js process handles every
 * status-line update, eliminating per-cycle spawn overhead on Windows.
 */
export function readStdinLoop(handler: (data: StatusLineData) => void | Promise<void>): void {
  if (process.stdin.isTTY) {
    process.exit(0);
  }

  let buffer = "";
  let pending = Promise.resolve();

  process.stdin.setEncoding("utf8");

  process.stdin.on("data", (chunk: string) => {
    buffer += chunk;
    drain();
  });

  process.stdin.on("end", () => {
    drain(); // last attempt with any remaining bytes
    pending.finally(() => process.exit(0));
  });

  process.stdin.on("error", () => {
    pending.finally(() => process.exit(0));
  });

  function drain() {
    while (true) {
      const frame = takeJsonFrame(buffer);
      if (!frame) break;

      buffer = frame.rest;
      try {
        const data = JSON.parse(frame.raw) as StatusLineData;
        pending = pending
          .then(() => handler(data))
          .catch(() => {});
      } catch {}
    }
  }
}

function takeJsonFrame(input: string): { raw: string; rest: string } | null {
  const trimmedStart = input.search(/\S/);
  if (trimmedStart === -1) return null;

  let depth = 0;
  let inString = false;
  let escaped = false;
  let start = -1;

  for (let i = trimmedStart; i < input.length; i++) {
    const ch = input[i];

    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === "\"") {
        inString = false;
      }
      continue;
    }

    if (ch === "\"") {
      inString = true;
      continue;
    }

    if (ch === "{" || ch === "[") {
      if (depth === 0) start = i;
      depth++;
      continue;
    }

    if (ch === "}" || ch === "]") {
      depth--;
      if (depth === 0 && start !== -1) {
        return {
          raw: input.slice(start, i + 1),
          rest: input.slice(i + 1),
        };
      }
    }
  }

  return null;
}
