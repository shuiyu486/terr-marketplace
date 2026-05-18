export interface StatusLineData {
  model: {
    display_name: string;
  };
  context_window: {
    used_percentage: number;
    context_window_size: number;
    total_input_tokens: number;
    total_output_tokens: number;
  };
  effort: {
    level: string;
  };
  transcript_path: string;
  workspace?: {
    current_dir?: string;
    project_dir?: string;
  };
  cwd?: string;
}

export interface ServerToolUse {
  web_search_requests?: number;
  web_fetch_requests?: number;
}

export interface UsageEntry {
  input_tokens: number;
  output_tokens: number;
  cache_creation_input_tokens: number;
  cache_read_input_tokens: number;
  server_tool_use_input_tokens?: number;
  server_tool_use?: ServerToolUse;
  service_tier?: string;
}

export interface TranscriptMessage {
  type: string;
  message?: {
    type?: string;
    role?: string;
    usage?: UsageEntry;
  };
  usage?: UsageEntry;
}

export interface SessionCache {
  lineNum: number;
  lastIn: number;
  lastOut: number;
  lastCacheCreate: number;
  lastCacheRead: number;
  sesApiIn: number;
  sesApiOut: number;
}

export interface Config {
  showEffort: boolean;
  showTokensLine: boolean;
  showPath: boolean;
  ctxWarnThreshold: number;
  ctxDangerThreshold: number;
}