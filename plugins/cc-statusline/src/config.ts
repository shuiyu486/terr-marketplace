import * as fs from "fs";
import * as os from "os";
import * as path from "path";

export interface Config {
  showEffort: boolean;
  showTokensLine: boolean;
  showPath: boolean;
  ctxWarnThreshold: number;
  ctxDangerThreshold: number;
  showToolActivity: boolean;
  showRunningTools: boolean;
  showCompletedTools: boolean;
  showAgentTracking: boolean;
  agentDisplayMode: "compact" | "multiline";
  showTodoProgress: boolean;
  showUsageLimits: boolean;
  codexProbeIntervalMinutes: number;
}

export const DEFAULT_CONFIG: Readonly<Config> = {
  showEffort: true,
  showTokensLine: true,
  showPath: true,
  ctxWarnThreshold: 70,
  ctxDangerThreshold: 90,
  showToolActivity: true,
  showRunningTools: true,
  showCompletedTools: true,
  showAgentTracking: true,
  agentDisplayMode: "compact",
  showTodoProgress: true,
  showUsageLimits: true,
  codexProbeIntervalMinutes: 3,
};

export interface ConfigMigrationResult {
  status: "created" | "migrated" | "reset_corrupt";
  configPath: string;
  backupPath?: string;
}

export function getClaudeConfigDir(env: NodeJS.ProcessEnv = process.env): string {
  return env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");
}

export function getConfigPath(env: NodeJS.ProcessEnv = process.env): string {
  return path.join(getClaudeConfigDir(env), "cc-statusline.json");
}

export function normalizeConfig(input: unknown): Config {
  const source = isRecord(input) ? input : {};
  const config: Config = { ...DEFAULT_CONFIG };

  config.showEffort = booleanValue(source.showEffort, DEFAULT_CONFIG.showEffort);
  config.showTokensLine = booleanValue(source.showTokensLine, DEFAULT_CONFIG.showTokensLine);
  config.showPath = booleanValue(source.showPath, DEFAULT_CONFIG.showPath);
  config.ctxWarnThreshold = numberValue(source.ctxWarnThreshold, DEFAULT_CONFIG.ctxWarnThreshold);
  config.ctxDangerThreshold = numberValue(source.ctxDangerThreshold, DEFAULT_CONFIG.ctxDangerThreshold);
  config.showToolActivity = booleanValue(source.showToolActivity, DEFAULT_CONFIG.showToolActivity);
  config.showRunningTools = booleanValue(source.showRunningTools, DEFAULT_CONFIG.showRunningTools);
  config.showCompletedTools = booleanValue(source.showCompletedTools, DEFAULT_CONFIG.showCompletedTools);
  config.showAgentTracking = booleanValue(source.showAgentTracking, DEFAULT_CONFIG.showAgentTracking);
  config.agentDisplayMode = source.agentDisplayMode === "multiline" ? "multiline" : DEFAULT_CONFIG.agentDisplayMode;
  config.showTodoProgress = booleanValue(source.showTodoProgress, DEFAULT_CONFIG.showTodoProgress);
  config.showUsageLimits = booleanValue(source.showUsageLimits, DEFAULT_CONFIG.showUsageLimits);
  config.codexProbeIntervalMinutes = clamp(
    integerValue(source.codexProbeIntervalMinutes, DEFAULT_CONFIG.codexProbeIntervalMinutes),
    1,
    10,
  );

  return config;
}

export function loadConfig(): Config {
  try {
    return normalizeConfig(JSON.parse(fs.readFileSync(getConfigPath(), "utf8")));
  } catch {
    return { ...DEFAULT_CONFIG };
  }
}

export function writeCompleteConfig(config: Config, configPath = getConfigPath()): void {
  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  fs.writeFileSync(configPath, JSON.stringify(normalizeConfig(config), null, 2) + "\n", "utf8");
}

export function migrateConfigFile(configPath = getConfigPath()): ConfigMigrationResult {
  fs.mkdirSync(path.dirname(configPath), { recursive: true });

  if (!fs.existsSync(configPath)) {
    writeCompleteConfig({ ...DEFAULT_CONFIG }, configPath);
    return { status: "created", configPath };
  }

  try {
    const parsed = JSON.parse(fs.readFileSync(configPath, "utf8"));
    if (!isRecord(parsed)) throw new Error("config root must be an object");
    writeCompleteConfig(normalizeConfig(parsed), configPath);
    return { status: "migrated", configPath };
  } catch {
    const backupPath = `${configPath}.bak-${timestamp()}`;
    fs.copyFileSync(configPath, backupPath);
    writeCompleteConfig({ ...DEFAULT_CONFIG }, configPath);
    return { status: "reset_corrupt", configPath, backupPath };
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function booleanValue(value: unknown, fallback: boolean): boolean {
  return typeof value === "boolean" ? value : fallback;
}

function numberValue(value: unknown, fallback: number): number {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function integerValue(value: unknown, fallback: number): number {
  const n = Number.parseInt(String(value), 10);
  return Number.isFinite(n) ? n : fallback;
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

function timestamp(): string {
  return new Date().toISOString().replace(/[:.]/g, "-");
}
