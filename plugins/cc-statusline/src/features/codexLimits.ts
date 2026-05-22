import * as fs from "fs";
import * as http from "http";
import * as https from "https";
import * as os from "os";
import * as path from "path";
import type { Config, StatusLineData } from "../types";

const DEFAULT_PROBE_INTERVAL_MINUTES = 3;
const MIN_PROBE_INTERVAL_MINUTES = 1;
const MAX_PROBE_INTERVAL_MINUTES = 10;
const FALLBACK_CACHE_MAX_AGE_MS = 24 * 60 * 60 * 1000;
const CACHE_PATH = path.join(os.tmpdir(), "cc-statusline-codex-limits.json");
const SETTINGS_PATH = path.join(os.homedir(), ".claude", "settings.json");

type RateLimits = NonNullable<StatusLineData["rate_limits"]>;

interface CachedLimits {
  ts: number;
  rate_limits: RateLimits;
}

interface ProbeEnv {
  baseUrl: string;
  token: string;
  model: string;
}

export interface CodexLimitsService {
  getSnapshot(data: StatusLineData): RateLimits | null;
  ensureFresh(data: StatusLineData, opts: { maxWaitMs: number }): Promise<RateLimits | null>;
}

export function createCodexLimitsService(cfg: Config): CodexLimitsService {
  let cached: CachedLimits | null = loadCache();
  let lastProbeAt = 0;
  let inflight: Promise<RateLimits | null> | null = null;

  function getSnapshot(data: StatusLineData): RateLimits | null {
    if (data.rate_limits?.five_hour) return data.rate_limits;
    if (!cached || Date.now() - cached.ts > FALLBACK_CACHE_MAX_AGE_MS) return null;
    if (!isLocalProxyUrl(claudeEnv().ANTHROPIC_BASE_URL)) return null;
    return cached.rate_limits;
  }

  async function ensureFresh(
    data: StatusLineData,
    opts: { maxWaitMs: number },
  ): Promise<RateLimits | null> {
    const snapshot = getSnapshot(data);
    const promise = startProbe(data);

    if (snapshot) {
      if (!promise || opts.maxWaitMs <= 0) return snapshot;
      return (await waitFor(promise, opts.maxWaitMs)) ?? snapshot;
    }

    if (!promise) return null;
    if (opts.maxWaitMs <= 0) return null;

    return waitFor(promise, opts.maxWaitMs);
  }

  function refreshInBackground(data: StatusLineData): void {
    startProbe(data);
  }

  function startProbe(data: StatusLineData): Promise<RateLimits | null> | null {
    if (inflight) return inflight;
    if (Date.now() - lastProbeAt < probeIntervalMs(cfg)) return null;

    const env = probeEnv(data);
    if (!env) return null;

    lastProbeAt = Date.now();
    inflight = probe(env.baseUrl, env.token, env.model)
      .then((limits) => {
        if (limits) saveCache(limits);
        return limits;
      })
      .catch(() => null)
      .finally(() => {
        inflight = null;
      });
    return inflight;
  }

  function saveCache(limits: RateLimits): void {
    cached = { ts: Date.now(), rate_limits: limits };
    try {
      fs.writeFileSync(CACHE_PATH, JSON.stringify(cached), "utf8");
    } catch {}
  }

  return { getSnapshot, ensureFresh };
}

function loadCache(): CachedLimits | null {
  try {
    const parsed = JSON.parse(fs.readFileSync(CACHE_PATH, "utf8")) as CachedLimits;
    if (!parsed.rate_limits?.five_hour) return null;
    return parsed;
  } catch {
    return null;
  }
}

function waitFor<T>(promise: Promise<T>, timeoutMs: number): Promise<T | null> {
  return new Promise((resolve) => {
    const timer = setTimeout(() => resolve(null), timeoutMs);
    promise.then(
      (value) => {
        clearTimeout(timer);
        resolve(value);
      },
      () => {
        clearTimeout(timer);
        resolve(null);
      },
    );
  });
}

function probeIntervalMs(cfg: Config): number {
  const minutes = Number.isFinite(cfg.codexProbeIntervalMinutes)
    ? cfg.codexProbeIntervalMinutes
    : DEFAULT_PROBE_INTERVAL_MINUTES;
  return Math.min(
    MAX_PROBE_INTERVAL_MINUTES,
    Math.max(MIN_PROBE_INTERVAL_MINUTES, minutes),
  ) * 60 * 1000;
}

function probeEnv(data: StatusLineData): ProbeEnv | null {
  const env = claudeEnv();
  const baseUrl = env.ANTHROPIC_BASE_URL;
  const token = env.ANTHROPIC_AUTH_TOKEN || env.ANTHROPIC_API_KEY;
  const model = env.ANTHROPIC_DEFAULT_SONNET_MODEL || data.model?.display_name;
  if (!baseUrl || !token || !model || !isLocalProxyUrl(baseUrl)) return null;
  return { baseUrl, token, model };
}

function isLocalProxyUrl(baseUrl: string | undefined): boolean {
  if (!baseUrl) return false;
  try {
    const host = new URL(baseUrl).hostname.toLowerCase();
    return host === "127.0.0.1" || host === "localhost" || host === "::1";
  } catch {
    return false;
  }
}

function claudeEnv(): NodeJS.ProcessEnv {
  const merged: NodeJS.ProcessEnv = {};
  try {
    const settings = JSON.parse(fs.readFileSync(SETTINGS_PATH, "utf8")) as { env?: Record<string, string> };
    Object.assign(merged, settings.env);
  } catch {}

  for (const [key, value] of Object.entries(process.env)) {
    if (value) merged[key] = value;
  }
  return merged;
}

function probe(baseUrl: string, token: string, model: string): Promise<RateLimits | null> {
  return new Promise((resolve) => {
    let url: URL;
    try {
      url = new URL("/v1/messages", baseUrl.endsWith("/") ? baseUrl : `${baseUrl}/`);
    } catch {
      resolve(null);
      return;
    }

    const body = JSON.stringify({
      model,
      max_tokens: 1,
      messages: [{ role: "user", content: "OK" }],
    });

    const client = url.protocol === "https:" ? https : http;
    const req = client.request(url, {
      method: "POST",
      timeout: 120000,
      headers: {
        "x-api-key": token,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "content-length": Buffer.byteLength(body),
      },
    }, (res) => {
      res.resume();
      res.on("end", () => resolve(parseCodexHeaders(res.headers)));
    });

    req.on("error", () => resolve(null));
    req.on("timeout", () => {
      req.destroy();
      resolve(null);
    });
    req.write(body);
    req.end();
  });
}

function parseCodexHeaders(headers: http.IncomingHttpHeaders): RateLimits | null {
  const primaryUsed = numberHeader(headers, "x-codex-primary-used-percent");
  const primaryReset = numberHeader(headers, "x-codex-primary-reset-at");
  if (primaryUsed === null || primaryReset === null) return null;

  const limits: RateLimits = {
    five_hour: {
      used_percentage: primaryUsed,
      resets_at: new Date(primaryReset * 1000).toISOString(),
    },
  };

  const secondaryUsed = numberHeader(headers, "x-codex-secondary-used-percent");
  const secondaryReset = numberHeader(headers, "x-codex-secondary-reset-at");
  if (secondaryUsed !== null && secondaryReset !== null) {
    limits.seven_day = {
      used_percentage: secondaryUsed,
      resets_at: new Date(secondaryReset * 1000).toISOString(),
    };
  }

  return limits;
}

function numberHeader(headers: http.IncomingHttpHeaders, name: string): number | null {
  const value = headers[name];
  const raw = Array.isArray(value) ? value[0] : value;
  if (!raw) return null;
  const n = Number(raw);
  return Number.isFinite(n) ? n : null;
}
