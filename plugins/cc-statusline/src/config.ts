import * as fs from "fs";
import * as os from "os";
import * as path from "path";

const BUILTIN_CODEX_PROBE_HOSTS = ["127.0.0.1", "localhost", "::1"] as const;

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
  codexProbeAllowedHosts: string[];
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
  codexProbeAllowedHosts: [],
};

export interface ConfigMigrationResult {
  status: "created" | "migrated" | "reset_corrupt";
  configPath: string;
  backupPath?: string;
}

export interface AllowCodexProbeHostResult {
  status: "added" | "already_allowed" | "builtin" | "invalid";
  host?: string;
  config: Config;
  configPath: string;
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
  config.codexProbeAllowedHosts = normalizeHostList(source.codexProbeAllowedHosts);

  return config;
}

export function loadConfig(): Config {
  return loadConfigFromPath(getConfigPath());
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

export function updateConfigFile(patch: Partial<Config>, configPath = getConfigPath()): Config {
  try {
    migrateConfigFile(configPath);
  } catch {}
  const current = loadConfigFromPath(configPath);
  const next = normalizeConfig({ ...current, ...patch });
  writeCompleteConfig(next, configPath);
  return next;
}

export function allowCodexProbeHost(hostOrUrl: string, configPath = getConfigPath()): AllowCodexProbeHostResult {
  try {
    migrateConfigFile(configPath);
  } catch {}
  const config = loadConfigFromPath(configPath);
  const host = normalizeCodexProbeHost(hostOrUrl);
  if (!host) return { status: "invalid", config, configPath };
  if (isBuiltinCodexProbeHost(host)) return { status: "builtin", host, config, configPath };
  if (config.codexProbeAllowedHosts.includes(host)) {
    return { status: "already_allowed", host, config, configPath };
  }

  const next = updateConfigFile({ codexProbeAllowedHosts: [...config.codexProbeAllowedHosts, host] }, configPath);
  return { status: "added", host, config: next, configPath };
}

export function normalizeHostname(input: unknown): string | null {
  return parseHostParts(input)?.hostname ?? null;
}

export function normalizeCodexProbeHost(input: unknown): string | null {
  const parts = parseHostParts(input);
  if (!parts) return null;
  return parts.port ? formatHostWithPort(parts.hostname, parts.port) : parts.hostname;
}

export function normalizeHostList(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  const hosts: string[] = [];
  const seen = new Set<string>();
  for (const item of value) {
    const host = normalizeCodexProbeHost(item);
    if (!host || seen.has(host)) continue;
    seen.add(host);
    hosts.push(host);
  }
  return hosts;
}

export function getBuiltinCodexProbeHosts(): readonly string[] {
  return BUILTIN_CODEX_PROBE_HOSTS;
}

export function isBuiltinCodexProbeHost(host: string): boolean {
  return BUILTIN_CODEX_PROBE_HOSTS.includes(normalizeHostname(host) as typeof BUILTIN_CODEX_PROBE_HOSTS[number]);
}

export function isCodexProbeAllowedHost(config: Config, host: string): boolean {
  const normalizedHost = normalizeHostname(host);
  const normalizedHostPort = normalizeCodexProbeHost(host);
  if (!normalizedHost || !normalizedHostPort) return false;
  return isBuiltinCodexProbeHost(normalizedHost)
    || config.codexProbeAllowedHosts.includes(normalizedHostPort);
}

function loadConfigFromPath(configPath: string): Config {
  try {
    return normalizeConfig(JSON.parse(fs.readFileSync(configPath, "utf8")));
  } catch {
    return { ...DEFAULT_CONFIG };
  }
}

interface HostParts {
  hostname: string;
  port: string;
}

function parseHostParts(input: unknown): HostParts | null {
  if (typeof input !== "string") return null;
  let raw = input.trim().toLowerCase();
  if (!raw) return null;

  if (raw === "::1") return { hostname: raw, port: "" };
  if (raw.startsWith("[") && raw.includes("]") && !raw.includes("://")) {
    const bracketEnd = raw.indexOf("]");
    const hostname = normalizeParsedHostname(raw.slice(1, bracketEnd));
    const rest = raw.slice(bracketEnd + 1);
    const port = rest.startsWith(":") ? normalizePort(rest.slice(1)) : "";
    return hostname ? { hostname, port } : null;
  }

  let rawForUrl = raw;
  let url = parseUrl(rawForUrl);
  if ((!url || !url.hostname) && !raw.includes("://")) {
    rawForUrl = `http://${raw}`;
    url = parseUrl(rawForUrl);
  }
  if (!url) return null;

  const hostname = normalizeParsedHostname(url.hostname);
  if (!hostname) return null;
  return { hostname, port: extractExplicitPort(rawForUrl) || normalizePort(url.port) };
}

function parseUrl(raw: string): URL | null {
  try {
    return new URL(raw);
  } catch {
    return null;
  }
}

function normalizeParsedHostname(hostname: string): string | null {
  let host = hostname.trim().toLowerCase();
  if (host.startsWith("[") && host.endsWith("]")) host = host.slice(1, -1);
  host = host.replace(/\.+$/g, "");
  return host || null;
}

function extractExplicitPort(rawUrl: string): string {
  const authority = rawUrl.replace(/^[a-z][a-z\d+.-]*:\/\//i, "").split(/[/?#]/, 1)[0];
  if (authority.startsWith("[")) {
    const bracketEnd = authority.indexOf("]");
    return bracketEnd >= 0 && authority[bracketEnd + 1] === ":"
      ? normalizePort(authority.slice(bracketEnd + 2))
      : "";
  }

  const colon = authority.lastIndexOf(":");
  if (colon < 0 || authority.indexOf(":") !== colon) return "";
  return normalizePort(authority.slice(colon + 1));
}

function normalizePort(port: string): string {
  return /^\d+$/.test(port) ? port : "";
}

function formatHostWithPort(hostname: string, port: string): string {
  return hostname.includes(":") ? `[${hostname}]:${port}` : `${hostname}:${port}`;
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
