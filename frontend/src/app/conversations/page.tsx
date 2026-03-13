"use client";

import { useEffect, useState } from "react";
import { api, ConversationItem } from "@/lib/api";

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<ConversationItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<number | null>(null);

  useEffect(() => {
    api
      .getConversations(100)
      .then((data) => {
        setConversations(data.conversations);
        setTotal(data.total);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Agent Conversations</h1>
        <span className="text-xs text-gray-500">
          {total} total conversations
        </span>
      </div>

      {loading ? (
        <p className="text-gray-500 text-sm animate-pulse">
          Loading conversations...
        </p>
      ) : conversations.length === 0 ? (
        <div className="card">
          <p className="text-gray-500 text-sm">
            No conversations yet. Conversations appear when users interact with
            @claw in Slack.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {conversations.map((conv) => (
            <div key={conv.id} className="card">
              <button
                onClick={() =>
                  setExpanded(expanded === conv.id ? null : conv.id)
                }
                className="w-full text-left"
              >
                <div className="flex items-center gap-3 mb-2">
                  <span className="badge-blue">{conv.user_id || "user"}</span>
                  {conv.channel && (
                    <span className="text-xs text-gray-500">
                      #{conv.channel}
                    </span>
                  )}
                  <time className="text-xs text-gray-600 ml-auto">
                    {new Date(conv.created_at).toLocaleString()}
                  </time>
                </div>
                <p className="text-sm text-gray-200 truncate">
                  {conv.user_message}
                </p>
              </button>

              {expanded === conv.id && (
                <div className="mt-4 space-y-3 border-t border-border pt-4">
                  <div>
                    <span className="text-[10px] uppercase tracking-widest text-gray-500">
                      User
                    </span>
                    <p className="text-sm text-gray-300 mt-1 whitespace-pre-wrap">
                      {conv.user_message}
                    </p>
                  </div>
                  <div>
                    <span className="text-[10px] uppercase tracking-widest text-gray-500">
                      Agent
                    </span>
                    <p className="text-sm text-gray-300 mt-1 whitespace-pre-wrap">
                      {conv.agent_response}
                    </p>
                  </div>
                  {conv.tools_used.length > 0 && (
                    <div>
                      <span className="text-[10px] uppercase tracking-widest text-gray-500">
                        Tools Used
                      </span>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {conv.tools_used.map((tool, i) => (
                          <span key={i} className="badge-gray font-mono">
                            {tool}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
