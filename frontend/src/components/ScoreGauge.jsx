export default function ScoreGauge({ score }) {
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const color = score >= 75 ? "#10b981" : score >= 50 ? "#f59e0b" : "#f43f5e";

  return (
    <div className="relative flex h-44 w-44 shrink-0 items-center justify-center">
      <svg width="176" height="176" viewBox="0 0 180 180" className="-rotate-90">
        <circle cx="90" cy="90" r={radius} fill="none" stroke="#334155" strokeWidth="12" />
        <circle
          cx="90"
          cy="90"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="14"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.8s ease" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-bold tracking-tight text-white">{Math.round(score)}</span>
        <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400">out of 100</span>
      </div>
    </div>
  );
}
