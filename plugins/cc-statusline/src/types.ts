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
  rate_limits?: {
    five_hour?: {
      used_percentage: number;
      resets_at: string | number;
    };
    seven_day?: {
      used_percentage: number;
      resets_at: string | number;
    };
  };
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

export interface ContentBlock {
  type: string;
  id?: string;
  name?: string;
  input?: Record<string, unknown>;
  tool_use_id?: string;
  is_error?: boolean;
}

export interface TranscriptMessage {
  type: string;
  message?: {
    type?: string;
    role?: string;
    usage?: UsageEntry;
    content?: ContentBlock[];
  };
  usage?: UsageEntry;
}

// --- v2 cache (JSON with version marker) ---
export interface ToolEvent {
  id: string;
  name: string;
  target: string;
  status: "running" | "completed";
  seenAt: number;
}

export interface AgentEvent {
  id: string;
  type: string;
  model: string;
  description: string;
  status: "running" | "completed";
  startTime: number;
  endTime?: number;
}

export interface TodoItem {
  id: string;
  subject: string;
  status: string;
}

export interface SessionCacheV2 {
  version: 2;
  sessionKey?: string;
  lineNum: number;
  lastIn: number;
  lastOut: number;
  lastCacheCreate: number;
  lastCacheRead: number;
  sesIn: number;
  sesOut: number;
  apiIn: number;
  apiOut: number;
  tools: ToolEvent[];
  agents: AgentEvent[];
  todos: TodoItem[];
  todoCompleted: number;
  todoTotal: number;
}

export interface ParseResult {
  sesIn: number;
  sesOut: number;
  apiIn: number;
  apiOut: number;
  tools: ToolEvent[];
  agents: AgentEvent[];
  todos: TodoItem[];
  todoCompleted: number;
  todoTotal: number;
}

export type { Config } from "./config";
