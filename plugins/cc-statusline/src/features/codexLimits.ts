import * as fs from "fs";
import * as http from "http";
import * as https from "https";
import * as os from "os";
import * as path from "path";
import type { StatusLineData } from "../types";

const PROBE_INTERVAL_MS = 5 * 60 * 1000;
const CACHE_MAX_AGE_MS = 60 * 60 * 1000;
const CACHE_PATH = path.join(os.tmpdir(), "cc-statusline-codex-limits.json");
const SETTINGS_PATH = path.join(os.homedir(), ".claude", "settings.json");

type RateLimits = NonNullable<StatusLineData["rate_limits"]>;

interface CachedLimits {
  ts: number;
  rate_limits: RateLimits;
}

let cached: CachedLimits | null = loadCache();
let lastProbeAt = 0;
let probing = false;

export function withCodexLimitFallback(data: StatusLineData): StatusLineData {
  if (data.rate_limits?.five_hour) return data;
  if (!cached || Date.now() - cached.ts > CACHE_MAX_AGE_MS) return data;
  return { ...data, rate_limits: cached.rate_limits };
}

export function maybeProbeCodexLimits(data: StatusLineData): void {
  if (data.rate_limits?.five_hour || probing) return;
  if (Date.now() - lastProbeAt < PROBE_INTERVAL_MS) return;

  const env = claudeEnv();
  const baseUrl = env.ANTHROPIC_BASE_URL;
  const token = env.ANTHROPIC_AUTH_TOKEN || env.ANTHROPIC_API_KEY;
  const model = env.ANTHROPIC_DEFAULT_SONNET_MODEL || data.model?.display_name;
  if (!baseUrl || !token || !model) return;

  lastProbeAt = Date.now();
  probing = true;
  probe(baseUrl, token, model)
    .then((limits) => {
      if (!limits) return;
      cached = { ts: Date.now(), rate_limits: limits };
      fs.writeFileSync(CACHE_PATH, JSON.stringify(cached), "utf8");
    })
    .catch(() => {})
    .finally(() => {
      probing = false;
    });
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
