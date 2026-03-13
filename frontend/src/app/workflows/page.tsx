"use client";

import { useEffect, useState } from "react";
import { api, WorkflowDef } from "@/lib/api";

export default function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<WorkflowDef[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getWorkflows()
      .then((data) => setWorkflows(data.workflows))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Workflows</h1>

      {loading ? (
        <p className="text-gray-500 text-sm animate-pulse">
          Loading workflows...
        </p>
      ) : workflows.length === 0 ? (
        <div className="card">
          <p className="text-gray-500 text-sm">
            No workflows loaded. Add YAML workflow definitions to the workflows/
            directory.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {workflows.map((wf) => (
            <div key={wf.name} className="card">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-gray-100">
                  {wf.name}
                </h3>
                <span
                  className={wf.enabled ? "badge-green" : "badge-gray"}
                >
                  {wf.enabled ? "enabled" : "disabled"}
                </span>
              </div>
              {wf.description && (
                <p className="text-xs text-gray-400 mb-3">{wf.description}</p>
              )}
              <div className="mb-3">
                <span className="text-[10px] uppercase tracking-widest text-gray-500">
                  Trigger
                </span>
                <p className="text-xs font-mono text-accent mt-0.5">
                  {wf.trigger}
                </p>
              </div>
              <div>
                <span className="text-[10px] uppercase tracking-widest text-gray-500">
                  Actions
                </span>
                <ol className="mt-1 space-y-1">
                  {wf.actions.map((action, i) => (
                    <li
                      key={i}
                      className="flex items-center gap-2 text-xs text-gray-300"
                    >
                      <span className="text-gray-600 w-4 text-right">
                        {i + 1}.
                      </span>
                      <code className="text-accent/80">{action.tool}</code>
                      {action.description && (
                        <span className="text-gray-500 truncate">
                          — {action.description}
                        </span>
                      )}
                    </li>
                  ))}
                </ol>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
