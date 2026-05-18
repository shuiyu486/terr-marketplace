import type { StatusLineData } from "./types";

const STDIN_TIMEOUT_MS = 500;

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
      // Try incremental parse
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
