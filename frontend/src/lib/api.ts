const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

async function fetchJSON<T>(path: string, params?: Record<string, string>): Promise<T> {
  const url = new URL(path, API_BASE);
  if (params) {
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  }
  const res = await fetch(url.toString(), {
    cache: "no-store",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

export interface SystemStatus {
  ironclaw: { status: string; error?: string };
  database: { status: string; error?: string };
  integrations: Record<string, { connected: boolean }>;
}

export interface EventItem {
  id: number;
  event_type: string;
  source: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export interface WorkflowDef {
  name: string;
  trigger: string;
  description: string;
  actions: { tool: string; description: string; args: Record<string, unknown> }[];
  enabled: boolean;
}

export interface WorkflowRunItem {
  id: number;
  workflow_name: string;
  trigger_event: string;
  status: string;
  result: unknown;
  started_at: string;
  finished_at: string | null;
}

export interface ToolItem {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
}

export interface ConversationItem {
  id: number;
  conversation_id: string;
  user_id: string;
  channel: string;
  user_message: string;
  agent_response: string;
  tools_used: string[];
  created_at: string;
}

export interface ModelConfig {
  current_provider: string;
  current_model: string;
  ollama_models: string[];
  openrouter_models: string[];
  openrouter_configured: boolean;
}

export interface ModelTestResult {
  ok: boolean;
  model: string;
  provider: string;
  response?: string;
  error?: string;
}

export interface LogItem {
  id: number;
  level: string;
  source: string;
  message: string;
  detail: string;
  created_at: string;
}

async function postJSON<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const url = new URL(path, API_BASE);
  const res = await fetch(url.toString(), {
    method: "POST",
    cache: "no-store",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || `API ${res.status}: ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  getStatus: () => fetchJSON<SystemStatus>("/api/status"),

  getEvents: (limit = 50, offset = 0) =>
    fetchJSON<{ events: EventItem[]; total: number }>("/api/events", {
      limit: String(limit),
      offset: String(offset),
    }),

  getWorkflows: () => fetchJSON<{ workflows: WorkflowDef[] }>("/api/workflows"),

  getWorkflowRuns: (limit = 50, offset = 0) =>
    fetchJSON<{ runs: WorkflowRunItem[]; total: number }>("/api/workflow-runs", {
      limit: String(limit),
      offset: String(offset),
    }),

  getTools: () => fetchJSON<{ tools: ToolItem[] }>("/api/tools"),

  getConversations: (limit = 50, offset = 0) =>
    fetchJSON<{ conversations: ConversationItem[]; total: number }>(
      "/api/agent-conversations",
      { limit: String(limit), offset: String(offset) }
    ),

  getModelConfig: () => fetchJSON<ModelConfig>("/api/model-config"),

  setModelConfig: (model: string, provider: string) =>
    postJSON<{ ok: boolean; provider: string; model: string }>(
      "/api/model-config",
      { model, provider }
    ),

  testModel: (model: string, provider: string) =>
    postJSON<ModelTestResult>("/api/model-config/test", { model, provider }),

  setOpenRouterKey: (api_key: string) =>
    postJSON<{ ok: boolean }>("/api/openrouter-key", { api_key }),

  getLogs: (limit = 100, offset = 0, search = "", level = "", source = "") => {
    const params: Record<string, string> = {
      limit: String(limit),
      offset: String(offset),
    };
    if (search) params.search = search;
    if (level) params.level = level;
    if (source) params.source = source;
    return fetchJSON<{ logs: LogItem[]; total: number }>("/api/logs", params);
  },
};
