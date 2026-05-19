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
export function readStdinLoop(handler: (data: StatusLineData) => void): void {
  if (process.stdin.isTTY) {
    process.exit(0);
  }

  let buffer = "";

  process.stdin.setEncoding("utf8");

  process.stdin.on("data", (chunk: string) => {
    buffer += chunk;
    drain();
  });

  process.stdin.on("end", () => {
    drain(); // last attempt with any remaining bytes
    process.exit(0);
  });

  process.stdin.on("error", () => {
    process.exit(0);
  });

  function drain() {
    while (true) {
      const trimmed = buffer.trim();
      if (!trimmed) break;

      try {
        const data = JSON.parse(trimmed) as StatusLineData;
        buffer = "";
        handler(data);
      } catch {
        // Incomplete JSON — wait for the next chunk
        break;
      }
    }
  }
}
