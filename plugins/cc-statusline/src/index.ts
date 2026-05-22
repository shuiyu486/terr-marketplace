import { readStdinLoop } from "./stdin";
import { parseTranscript } from "./transcript";
import { render } from "./render";
import { createCodexLimitsService } from "./features/codexLimits";
import type { Config } from "./types";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

const CONFIG_PATH = path.join(os.homedir(), ".claude", "cc-statusline.json");

const DEFAULT_CONFIG: Config = {
  showEffort: true,
  showTokensLine: true,
  showPath: true,
  ctxWarnThreshold: 70,
  ctxDangerThreshold: 90,
  showToolActivity: true,
  showRunningTools: true,
  showCompletedTools: true,
  showAgentTracking: true,
  showTodoProgress: true,
  showUsageLimits: true,
  codexProbeIntervalMinutes: 3,
};

function loadConfig(): Config {
  try {
    const raw = fs.readFileSync(CONFIG_PATH, "utf8");
    return { ...DEFAULT_CONFIG, ...JSON.parse(raw) };
  } catch {
    return DEFAULT_CONFIG;
  }
}

// Long-running mode: one Node.js process handles every ~300ms update.
// Eliminates per-cycle spawn overhead that exhausts the Windows Desktop Heap.
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
