interface StatusCardProps {
  title: string;
  status: string;
  error?: string;
}

export default function StatusCard({ title, status, error }: StatusCardProps) {
  const isOk = status === "healthy" || status === "connected" || status === "ok";
  const isUnknown = status === "unknown";

  return (
    <div className="card flex items-start gap-4">
      <div
        className={`mt-0.5 h-3 w-3 rounded-full ${
          isOk
            ? "bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.5)]"
            : isUnknown
            ? "bg-gray-500"
            : "bg-red-400 shadow-[0_0_8px_rgba(248,113,113,0.5)]"
        }`}
      />
      <div className="flex-1 min-w-0">
        <h3 className="text-sm font-medium text-gray-200">{title}</h3>
        <p
          className={`text-xs mt-0.5 ${
            isOk ? "text-emerald-400" : isUnknown ? "text-gray-500" : "text-red-400"
          }`}
        >
          {status}
        </p>
        {error && (
          <p className="text-xs text-red-400/70 mt-1 truncate">{error}</p>
        )}
      </div>
    </div>
  );
}
