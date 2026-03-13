"use client";

import { useEffect, useState } from "react";
import StatusCard from "@/components/StatusCard";
import ModelSelector from "@/components/ModelSelector";
import { api, SystemStatus } from "@/lib/api";

export default function StatusPage() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .getStatus()
      .then(setStatus)
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div>
        <h1 className="text-2xl font-bold mb-6">System Status</h1>
        <div className="card border-red-500/30">
          <p className="text-red-400 text-sm">
            Unable to reach backend: {error}
          </p>
          <p className="text-gray-500 text-xs mt-2">
            Ensure the backend is running on http://localhost:8080
          </p>
        </div>
      </div>
    );
  }

  if (!status) {
    return (
      <div>
        <h1 className="text-2xl font-bold mb-6">System Status</h1>
        <p className="text-gray-500 text-sm animate-pulse">Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">System Status</h1>

      <section className="mb-8">
        <h2 className="text-xs uppercase tracking-widest text-gray-500 mb-3">
          Core Services
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <StatusCard
            title="IronClaw Runtime"
            status={status.ironclaw.status}
            error={status.ironclaw.error}
          />
          <StatusCard
            title="PostgreSQL Database"
            status={status.database.status}
            error={status.database.error}
          />
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-xs uppercase tracking-widest text-gray-500 mb-3">
          AI Model
        </h2>
        <ModelSelector />
      </section>

      <section>
        <h2 className="text-xs uppercase tracking-widest text-gray-500 mb-3">
          Integrations
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(status.integrations).map(([name, info]) => (
            <StatusCard
              key={name}
              title={name.charAt(0).toUpperCase() + name.slice(1)}
              status={info.connected ? "connected" : "not configured"}
            />
          ))}
        </div>
      </section>
    </div>
  );
}
