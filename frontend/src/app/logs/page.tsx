"use client";

import { useCallback, useEffect, useState } from "react";
import { api, LogItem } from "@/lib/api";

const LEVELS = ["", "INFO", "WARN", "ERROR", "DEBUG"];
const LEVEL_COLORS: Record<string, string> = {
  INFO: "badge-blue",
  WARN: "badge-yellow",
  ERROR: "badge-red",
  DEBUG: "badge-gray",
};

export default function LogsPage() {
  const [logs, setLogs] = useState<LogItem[]>([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [level, setLevel] = useState("");
  const [source, setSource] = useState("");
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());
  const limit = 100;

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(timer);
  }, [search]);

  const fetchLogs = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.getLogs(limit, offset, debouncedSearch, level, source);
      setLogs(data.logs);
      setTotal(data.total);
    } catch {
      /* backend unreachable */
    } finally {
      setLoading(false);
    }
  }, [offset, debouncedSearch, level, source]);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  useEffect(() => {
    if (!autoRefresh) return;
    const id = setInterval(fetchLogs, 5000);
    return () => clearInterval(id);
  }, [autoRefresh, fetchLogs]);

  const toggleExpand = (id: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const totalPages = Math.ceil(total / limit);
  const currentPage = Math.floor(offset / limit) + 1;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Agent Logs</h1>
        <div className="flex items-center gap-3">
          <span className="text-xs text-gray-500">{total} entries</span>
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors ${
              autoRefresh
                ? "border-emerald-500/30 text-emerald-400 bg-emerald-500/5"
                : "border-border text-gray-400 hover:bg-surface-overlay"
            }`}
          >
            {autoRefresh ? "Live" : "Paused"}
          </button>
          <button
            onClick={fetchLogs}
            className="rounded-lg border border-border px-3 py-1.5 text-xs font-medium text-gray-400 hover:bg-surface-overlay transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>

      <div className="card mb-4">
        <div className="flex flex-wrap gap-3">
          <div className="flex-[3] min-w-[200px]">
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setOffset(0);
              }}
              placeholder="Search logs..."
              className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:border-accent focus:outline-none"
            />
          </div>
          <div className="min-w-[120px]">
            <select
              value={level}
              onChange={(e) => {
                setLevel(e.target.value);
                setOffset(0);
              }}
              className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-gray-200 focus:border-accent focus:outline-none"
            >
              <option value="">All Levels</option>
              {LEVELS.filter(Boolean).map((l) => (
                <option key={l} value={l}>
                  {l}
                </option>
              ))}
            </select>
          </div>
          <div className="min-w-[160px]">
            <input
              type="text"
              value={source}
              onChange={(e) => {
                setSource(e.target.value);
                setOffset(0);
              }}
              placeholder="Filter by source..."
              className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:border-accent focus:outline-none"
            />
          </div>
        </div>
      </div>

      {loading && logs.length === 0 ? (
        <p className="text-gray-500 text-sm animate-pulse">Loading...</p>
      ) : logs.length === 0 ? (
        <div className="card">
          <p className="text-gray-500 text-sm">
            {debouncedSearch || level || source
              ? "No logs match your filters."
              : "No logs recorded yet. Logs appear as webhooks, model switches, and agent actions occur."}
          </p>
        </div>
      ) : (
        <div className="space-y-1">
          {logs.map((log) => (
            <div
              key={log.id}
              className="card !p-3 cursor-pointer hover:bg-surface-overlay transition-colors"
              onClick={() => toggleExpand(log.id)}
            >
              <div className="flex items-start gap-3">
                <span className={LEVEL_COLORS[log.level] || "badge-gray"}>
                  {log.level}
                </span>
                <span className="text-xs text-gray-500 font-mono whitespace-nowrap">
                  {log.created_at
                    ? new Date(log.created_at).toLocaleTimeString()
                    : "—"}
                </span>
                <span className="text-xs text-accent/70 font-mono whitespace-nowrap">
                  {log.source}
                </span>
                <span className="text-sm text-gray-300 flex-1 truncate">
                  {log.message}
                </span>
              </div>
              {expanded.has(log.id) && log.detail && (
                <pre className="mt-2 ml-8 text-xs text-gray-500 bg-surface rounded-lg p-3 overflow-x-auto whitespace-pre-wrap">
                  {log.detail}
                </pre>
              )}
            </div>
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-3 mt-6">
          <button
            onClick={() => setOffset(Math.max(0, offset - limit))}
            disabled={offset === 0}
            className="rounded-lg border border-border px-3 py-1.5 text-xs text-gray-400 hover:bg-surface-overlay disabled:opacity-30 transition-colors"
          >
            Previous
          </button>
          <span className="text-xs text-gray-500">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setOffset(offset + limit)}
            disabled={offset + limit >= total}
            className="rounded-lg border border-border px-3 py-1.5 text-xs text-gray-400 hover:bg-surface-overlay disabled:opacity-30 transition-colors"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
