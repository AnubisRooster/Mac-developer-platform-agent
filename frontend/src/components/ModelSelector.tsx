"use client";

import { useEffect, useState } from "react";
import { api, ModelConfig } from "@/lib/api";

export default function ModelSelector() {
  const [config, setConfig] = useState<ModelConfig | null>(null);
  const [selectedProvider, setSelectedProvider] = useState("ollama");
  const [selectedModel, setSelectedModel] = useState("");
  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState(false);
  const [message, setMessage] = useState<{ type: "ok" | "error"; text: string } | null>(null);
  const [openrouterKey, setOpenrouterKey] = useState("");
  const [showKeyInput, setShowKeyInput] = useState(false);

  useEffect(() => {
    api.getModelConfig().then((c) => {
      setConfig(c);
      setSelectedProvider(c.current_provider);
      setSelectedModel(c.current_model);
    });
  }, []);

  if (!config) {
    return (
      <div className="card">
        <p className="text-gray-500 text-sm animate-pulse">Loading model config...</p>
      </div>
    );
  }

  const models =
    selectedProvider === "openrouter"
      ? config.openrouter_models
      : config.ollama_models;

  const handleTest = async () => {
    setTesting(true);
    setMessage(null);
    try {
      const result = await api.testModel(selectedModel, selectedProvider);
      if (result.ok) {
        setMessage({ type: "ok", text: `Model responded: "${result.response}"` });
      } else {
        setMessage({ type: "error", text: `Model unavailable: ${result.error}` });
      }
    } catch (e: any) {
      setMessage({ type: "error", text: e.message });
    } finally {
      setTesting(false);
    }
  };

  const handleApply = async () => {
    setLoading(true);
    setMessage(null);
    try {
      await api.setModelConfig(selectedModel, selectedProvider);
      setConfig({ ...config, current_model: selectedModel, current_provider: selectedProvider });
      setMessage({ type: "ok", text: `Switched to ${selectedProvider}/${selectedModel}` });
    } catch (e: any) {
      setMessage({ type: "error", text: e.message });
    } finally {
      setLoading(false);
    }
  };

  const handleSetKey = async () => {
    if (!openrouterKey.trim()) return;
    try {
      await api.setOpenRouterKey(openrouterKey.trim());
      setConfig({ ...config, openrouter_configured: true });
      setOpenrouterKey("");
      setShowKeyInput(false);
      setMessage({ type: "ok", text: "OpenRouter API key saved" });
    } catch (e: any) {
      setMessage({ type: "error", text: e.message });
    }
  };

  const isActive =
    selectedModel === config.current_model &&
    selectedProvider === config.current_provider;

  return (
    <div className="card space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-200">Model Configuration</h3>
        {config.current_model && (
          <span className="badge-blue">
            {config.current_provider}/{config.current_model}
          </span>
        )}
      </div>

      <div className="flex gap-3">
        <div className="flex-1 space-y-1.5">
          <label className="text-xs text-gray-500">Provider</label>
          <select
            value={selectedProvider}
            onChange={(e) => {
              const p = e.target.value;
              setSelectedProvider(p);
              const ml = p === "openrouter" ? config.openrouter_models : config.ollama_models;
              setSelectedModel(ml[0] || "");
              setMessage(null);
            }}
            className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-gray-200 focus:border-accent focus:outline-none"
          >
            <option value="ollama">Ollama (local)</option>
            <option value="openrouter">OpenRouter (cloud)</option>
          </select>
        </div>

        <div className="flex-[2] space-y-1.5">
          <label className="text-xs text-gray-500">Model</label>
          <select
            value={selectedModel}
            onChange={(e) => {
              setSelectedModel(e.target.value);
              setMessage(null);
            }}
            className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-gray-200 focus:border-accent focus:outline-none"
          >
            {models.map((m) => (
              <option key={m} value={m}>
                {m}
                {m === config.current_model && selectedProvider === config.current_provider
                  ? " (active)"
                  : ""}
              </option>
            ))}
          </select>
        </div>
      </div>

      {selectedProvider === "openrouter" && !config.openrouter_configured && (
        <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-3">
          <p className="text-xs text-amber-400 mb-2">
            OpenRouter requires an API key. Add it in .env as OPENROUTER_API_KEY or set it here:
          </p>
          {!showKeyInput ? (
            <button
              onClick={() => setShowKeyInput(true)}
              className="text-xs text-accent hover:text-accent-hover transition-colors"
            >
              Set API key...
            </button>
          ) : (
            <div className="flex gap-2">
              <input
                type="password"
                value={openrouterKey}
                onChange={(e) => setOpenrouterKey(e.target.value)}
                placeholder="sk-or-..."
                className="flex-1 rounded-lg border border-border bg-surface px-3 py-1.5 text-sm text-gray-200 focus:border-accent focus:outline-none"
              />
              <button
                onClick={handleSetKey}
                className="rounded-lg bg-accent px-3 py-1.5 text-xs font-medium text-white hover:bg-accent-hover transition-colors"
              >
                Save
              </button>
            </div>
          )}
        </div>
      )}

      <div className="flex gap-2">
        <button
          onClick={handleTest}
          disabled={testing || !selectedModel}
          className="rounded-lg border border-border px-4 py-2 text-xs font-medium text-gray-300 hover:bg-surface-overlay transition-colors disabled:opacity-40"
        >
          {testing ? "Testing..." : "Test Model"}
        </button>
        <button
          onClick={handleApply}
          disabled={loading || isActive || !selectedModel}
          className="rounded-lg bg-accent px-4 py-2 text-xs font-medium text-white hover:bg-accent-hover transition-colors disabled:opacity-40"
        >
          {loading ? "Switching..." : isActive ? "Active" : "Apply"}
        </button>
      </div>

      {message && (
        <p
          className={`text-xs ${
            message.type === "ok" ? "text-emerald-400" : "text-red-400"
          }`}
        >
          {message.text}
        </p>
      )}
    </div>
  );
}
