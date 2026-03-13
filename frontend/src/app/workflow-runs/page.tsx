"use client";

import { useEffect, useState } from "react";
import { api, WorkflowRunItem } from "@/lib/api";

function statusBadge(status: string) {
  switch (status) {
    case "completed":
      return "badge-green";
    case "failed":
      return "badge-red";
    case "running":
      return "badge-yellow";
    default:
      return "badge-gray";
  }
}

export default function WorkflowRunsPage() {
  const [runs, setRuns] = useState<WorkflowRunItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getWorkflowRuns(100)
      .then((data) => {
        setRuns(data.runs);
        setTotal(data.total);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Workflow Runs</h1>
        <span className="text-xs text-gray-500">{total} total runs</span>
      </div>

      {loading ? (
        <p className="text-gray-500 text-sm animate-pulse">Loading runs...</p>
      ) : runs.length === 0 ? (
        <div className="card">
          <p className="text-gray-500 text-sm">
            No workflow runs yet. Runs appear when events trigger workflows.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-left">
                <th className="pb-3 text-xs font-medium uppercase tracking-widest text-gray-500">
                  Workflow
                </th>
                <th className="pb-3 text-xs font-medium uppercase tracking-widest text-gray-500">
                  Trigger
                </th>
                <th className="pb-3 text-xs font-medium uppercase tracking-widest text-gray-500">
                  Status
                </th>
                <th className="pb-3 text-xs font-medium uppercase tracking-widest text-gray-500">
                  Started
                </th>
                <th className="pb-3 text-xs font-medium uppercase tracking-widest text-gray-500">
                  Finished
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {runs.map((run) => (
                <tr key={run.id} className="hover:bg-surface-overlay/50">
                  <td className="py-3 font-medium text-gray-200">
                    {run.workflow_name}
                  </td>
                  <td className="py-3 font-mono text-xs text-gray-400">
                    {run.trigger_event}
                  </td>
                  <td className="py-3">
                    <span className={statusBadge(run.status)}>
                      {run.status}
                    </span>
                  </td>
                  <td className="py-3 text-xs text-gray-500">
                    {run.started_at
                      ? new Date(run.started_at).toLocaleString()
                      : "—"}
                  </td>
                  <td className="py-3 text-xs text-gray-500">
                    {run.finished_at
                      ? new Date(run.finished_at).toLocaleString()
                      : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
