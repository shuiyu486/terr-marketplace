import { readStdin } from "./stdin";
import { parseTranscript } from "./transcript";
import { render } from "./render";
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
};

function loadConfig(): Config {
  try {
    const raw = fs.readFileSync(CONFIG_PATH, "utf8");
    return { ...DEFAULT_CONFIG, ...JSON.parse(raw) };
  } catch {
    return DEFAULT_CONFIG;
  }
}

async function main(): Promise<void> {
  const data = await readStdin();
  if (!data) {
    process.exit(0);
  }

  const cfg = loadConfig();
  const { sesApiIn, sesApiOut } = parseTranscript(data.transcript_path);
  const output = render(data, sesApiIn, sesApiOut, cfg);
  process.stdout.write(output);
}

main().catch(() => process.exit(0));
