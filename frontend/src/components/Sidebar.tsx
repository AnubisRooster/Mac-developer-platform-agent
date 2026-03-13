"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const nav = [
  { href: "/", label: "Status", icon: "◉" },
  { href: "/logs", label: "Logs", icon: "▤" },
  { href: "/events", label: "Events", icon: "⚡" },
  { href: "/workflows", label: "Workflows", icon: "⛓" },
  { href: "/workflow-runs", label: "Runs", icon: "▶" },
  { href: "/tools", label: "Tools", icon: "⚙" },
  { href: "/conversations", label: "Conversations", icon: "💬" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-30 flex w-56 flex-col border-r border-border bg-surface">
      <div className="flex h-14 items-center gap-2 border-b border-border px-5">
        <span className="text-lg font-bold tracking-tight text-accent">
          Claw
        </span>
        <span className="text-xs text-gray-500">Agent</span>
      </div>
      <nav className="flex-1 space-y-0.5 px-3 py-4">
        {nav.map((item) => {
          const active =
            item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
                active
                  ? "bg-accent/10 text-accent font-medium"
                  : "text-gray-400 hover:bg-surface-overlay hover:text-gray-200"
              }`}
            >
              <span className="w-5 text-center text-base">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="border-t border-border px-5 py-3">
        <p className="text-[10px] uppercase tracking-widest text-gray-600">
          IronClaw Runtime
        </p>
      </div>
    </aside>
  );
}
