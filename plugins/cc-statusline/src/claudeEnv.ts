import * as fs from "fs";
import * as path from "path";
import { getClaudeConfigDir, normalizeHostname } from "./config";

export function getClaudeSettingsPath(env: NodeJS.ProcessEnv = process.env): string {
  return path.join(getClaudeConfigDir(env), "settings.json");
}

export function getEffectiveClaudeEnv(env: NodeJS.ProcessEnv = process.env): NodeJS.ProcessEnv {
  const merged: NodeJS.ProcessEnv = {};
  try {
    const settings = JSON.parse(fs.readFileSync(getClaudeSettingsPath(env), "utf8")) as { env?: Record<string, string> };
    Object.assign(merged, settings.env);
  } catch {}

  for (const [key, value] of Object.entries(env)) {
    if (value !== undefined) merged[key] = value;
  }
  return merged;
}

export function getCurrentAnthropicBaseUrlHost(env: NodeJS.ProcessEnv = process.env): string | null {
  return normalizeHostname(getEffectiveClaudeEnv(env).ANTHROPIC_BASE_URL);
}
