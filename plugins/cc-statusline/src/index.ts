import { readStdinLoop } from "./stdin";
import { parseTranscript } from "./transcript";
import { render } from "./render";
import { createCodexLimitsService } from "./features/codexLimits";
import { loadConfig, migrateConfigFile } from "./config";
import * as fs from "fs";

// Long-running mode: one Node.js process handles every ~300ms update.
// Eliminates per-cycle spawn overhead that exhausts the Windows Desktop Heap.
try {
  migrateConfigFile();
} catch {}
const cfg = loadConfig();
const codexLimits = createCodexLimitsService(cfg);

function flush(msg: string): void {
  // Synchronous unbuffered write — pipe stdout doesn't auto-flush in Node.js.
  // Using fd 1 avoids the stream buffer so Claude Code sees each line immediately.
  fs.writeSync(1, msg + "\n");
}

readStdinLoop(async (data) => {
  try {
    const rateLimits = cfg.showUsageLimits
      ? await codexLimits.ensureFresh(data, { maxWaitMs: 3000 })
      : null;
    const ctx = parseTranscript(data.transcript_path);
    const output = render(rateLimits ? { ...data, rate_limits: rateLimits } : data, ctx, cfg);
    flush(output);
  } catch {
    // Skip failed updates — a single corrupt frame shouldn't kill the daemon
  }
});
