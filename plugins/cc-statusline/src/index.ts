import { readStdinLoop } from "./stdin";
import { parseTranscript } from "./transcript";
import { render } from "./render";
import { createCodexLimitsService, type CodexLimitsService } from "./features/codexLimits";
import { getConfigPath, loadConfig, migrateConfigFile, type Config } from "./config";
import * as fs from "fs";

// Long-running mode: one Node.js process handles every ~300ms update.
// Eliminates per-cycle spawn overhead that exhausts the Windows Desktop Heap.
try {
  migrateConfigFile();
} catch {}
let cfg = loadConfig();
let configMtime = configMtimeMs();
let codexLimits = createCodexLimitsService(cfg);

function flush(msg: string): void {
  // Synchronous unbuffered write — pipe stdout doesn't auto-flush in Node.js.
  // Using fd 1 avoids the stream buffer so Claude Code sees each line immediately.
  fs.writeSync(1, msg + "\n");
}

readStdinLoop(async (data) => {
  try {
    const current = currentRuntimeConfig();
    const rateLimits = current.cfg.showUsageLimits
      ? await current.codexLimits.ensureFresh(data, { maxWaitMs: 3000 })
      : null;
    const ctx = parseTranscript(data.transcript_path);
    const output = render(rateLimits ? { ...data, rate_limits: rateLimits } : data, ctx, current.cfg);
    flush(output);
  } catch {
    // Skip failed updates — a single corrupt frame shouldn't kill the daemon
  }
});

function currentRuntimeConfig(): { cfg: Config; codexLimits: CodexLimitsService } {
  const nextMtime = configMtimeMs();
  if (nextMtime !== configMtime) {
    cfg = loadConfig();
    codexLimits = createCodexLimitsService(cfg);
    configMtime = nextMtime;
  }
  return { cfg, codexLimits };
}

function configMtimeMs(): number {
  try {
    return fs.statSync(getConfigPath()).mtimeMs;
  } catch {
    return 0;
  }
}
