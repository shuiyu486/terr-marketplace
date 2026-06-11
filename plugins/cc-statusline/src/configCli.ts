import {
  allowCodexProbeHost,
  isBuiltinCodexProbeHost,
  isCodexProbeAllowedHost,
  loadConfig,
  migrateConfigFile,
  normalizeConfig,
  updateConfigFile,
} from "./config";
import { getCurrentAnthropicBaseUrlHost, getEffectiveClaudeEnv } from "./claudeEnv";

interface CliResult {
  ok: boolean;
  [key: string]: unknown;
}

function main(argv: string[]): void {
  const command = argv[2];
  try {
    switch (command) {
      case "read":
        print({ ok: true, config: loadConfig() });
        return;
      case "migrate":
        print({ ok: true, result: migrateConfigFile() });
        return;
      case "patch":
        print({ ok: true, config: updateConfigFile(normalizePatch(argv[3])) });
        return;
      case "suggest-probe-host":
        print(suggestProbeHost());
        return;
      case "allow-probe-host":
        print({ ok: true, result: allowCodexProbeHost(argv[3] || "") });
        return;
      default:
        print({ ok: false, error: `unknown command: ${command || ""}` });
        process.exitCode = 1;
    }
  } catch (error) {
    print({ ok: false, error: error instanceof Error ? error.message : String(error) });
    process.exitCode = 1;
  }
}

function suggestProbeHost(): CliResult {
  migrateConfigFile();
  const config = loadConfig();
  const env = getEffectiveClaudeEnv();
  const host = getCurrentAnthropicBaseUrlHost();
  if (!env.ANTHROPIC_BASE_URL) {
    return { ok: true, status: "no_base_url", shouldAsk: false, config };
  }
  if (!host) {
    return { ok: true, status: "invalid_base_url", shouldAsk: false, baseUrl: env.ANTHROPIC_BASE_URL, config };
  }
  const isBuiltin = isBuiltinCodexProbeHost(host);
  const isAllowed = isCodexProbeAllowedHost(config, host);
  return {
    ok: true,
    status: isBuiltin ? "builtin" : isAllowed ? "already_allowed" : "needs_confirmation",
    host,
    baseUrl: env.ANTHROPIC_BASE_URL,
    isBuiltin,
    isAllowed,
    shouldAsk: !isBuiltin && !isAllowed,
    config,
  };
}

function normalizePatch(raw: string | undefined): ReturnType<typeof normalizeConfig> {
  if (!raw) throw new Error("patch JSON is required");
  const parsed = JSON.parse(raw);
  return normalizeConfig({ ...loadConfig(), ...parsed });
}

function print(value: unknown): void {
  process.stdout.write(JSON.stringify(value, null, 2) + "\n");
}

main(process.argv);
