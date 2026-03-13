"use client";

import { useEffect, useState } from "react";
import { api, EventItem } from "@/lib/api";

function sourceBadge(source: string) {
  const colors: Record<string, string> = {
    github: "badge-blue",
    jira: "badge-yellow",
    jenkins: "badge-red",
    slack: "badge-green",
    system: "badge-gray",
  };
  return colors[source] || "badge-gray";
}

export default function EventsPage() {
  const [events, setEvents] = useState<EventItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getEvents(100)
      .then((data) => {
        setEvents(data.events);
        setTotal(data.total);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Event Stream</h1>
        <span className="text-xs text-gray-500">{total} total events</span>
      </div>

      {loading ? (
        <p className="text-gray-500 text-sm animate-pulse">Loading events...</p>
      ) : events.length === 0 ? (
        <div className="card">
          <p className="text-gray-500 text-sm">
            No events recorded yet. Events appear when webhooks fire or commands
            are processed.
          </p>
        </div>
      ) : (
        <div className="space-y-2">
          {events.map((ev) => (
            <div
              key={ev.id}
              className="card flex items-center gap-4 py-3 px-4"
            >
              <span className={sourceBadge(ev.source)}>{ev.source}</span>
              <span className="text-sm font-mono text-gray-200 flex-1 truncate">
                {ev.event_type}
              </span>
              <time className="text-xs text-gray-500 shrink-0">
                {new Date(ev.created_at).toLocaleString()}
              </time>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
