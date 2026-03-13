"use client";

import { useEffect, useState } from "react";
import { api, ToolItem } from "@/lib/api";

function connectorColor(name: string) {
  if (name.startsWith("github")) return "border-l-blue-500";
  if (name.startsWith("jira")) return "border-l-yellow-500";
  if (name.startsWith("slack")) return "border-l-green-500";
  if (name.startsWith("jenkins")) return "border-l-red-500";
  if (name.startsWith("confluence")) return "border-l-cyan-500";
  if (name.startsWith("gmail")) return "border-l-orange-500";
  return "border-l-accent";
}

export default function ToolsPage() {
  const [tools, setTools] = useState<ToolItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getTools()
      .then((data) => setTools(data.tools))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Tool Registry</h1>
        <span className="text-xs text-gray-500">{tools.length} tools</span>
      </div>

      {loading ? (
        <p className="text-gray-500 text-sm animate-pulse">Loading tools...</p>
      ) : tools.length === 0 ? (
        <div className="card">
          <p className="text-gray-500 text-sm">
            No tools registered. Tools are registered when the backend starts
            with configured integrations.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {tools.map((tool) => (
            <div
              key={tool.name}
              className={`card border-l-4 ${connectorColor(tool.name)}`}
            >
              <h3 className="text-sm font-mono font-semibold text-gray-100 mb-1">
                {tool.name}
              </h3>
              <p className="text-xs text-gray-400 mb-3">{tool.description}</p>
              {tool.parameters &&
                Object.keys(tool.parameters).length > 0 && (
                  <details className="group">
                    <summary className="text-[10px] uppercase tracking-widest text-gray-500 cursor-pointer hover:text-gray-400 transition-colors">
                      Parameters
                    </summary>
                    <pre className="mt-2 text-[11px] text-gray-500 bg-surface rounded-lg p-3 overflow-x-auto leading-relaxed">
                      {JSON.stringify(tool.parameters, null, 2)}
                    </pre>
                  </details>
                )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
