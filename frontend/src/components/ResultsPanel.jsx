import {
  AlertCircle,
  ArrowUpRight,
  CheckCircle2,
  ClipboardCheck,
  RefreshCw,
  Sparkles,
  Target,
} from "lucide-react";
import ScoreGauge from "./ScoreGauge";

function scoreLabel(score) {
  if (score >= 90) return { label: "Excellent match", tone: "text-emerald-300 bg-emerald-400/10 border-emerald-400/20" };
  if (score >= 75) return { label: "Strong foundation", tone: "text-emerald-300 bg-emerald-400/10 border-emerald-400/20" };
  if (score >= 60) return { label: "Room to improve", tone: "text-amber-300 bg-amber-400/10 border-amber-400/20" };
  return { label: "Needs attention", tone: "text-rose-300 bg-rose-400/10 border-rose-400/20" };
}

function categoryTone(value) {
  return value >= 75 ? "bg-emerald-400" : value >= 50 ? "bg-amber-400" : "bg-rose-400";
}

function CategoryBar({ label, value }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-slate-300">{label}</span>
        <span className="font-semibold text-white">{Math.round(value)}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-slate-700">
        <div className={`h-full rounded-full ${categoryTone(value)}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function SectionHeading({ icon: Icon, eyebrow, children }) {
  return (
    <div className="mb-5 flex items-start gap-3">
      <div className="rounded-lg bg-indigo-50 p-2 text-indigo-600">
        <Icon className="h-4 w-4" />
      </div>
      <div>
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-slate-400">{eyebrow}</p>
        <h2 className="mt-0.5 text-lg font-semibold text-slate-900">{children}</h2>
      </div>
    </div>
  );
}

export default function ResultsPanel({ result, onReset }) {
  const score = result.final_score;
  const status = scoreLabel(score);
  const totalSkills = result.matched_skills.length + result.missing_skills.length;
  const matchRate = totalSkills ? Math.round((result.matched_skills.length / totalSkills) * 100) : 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-sm font-semibold text-indigo-600">Analysis complete</p>
          <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-950">Your resume report</h1>
          <p className="mt-2 text-sm text-slate-500">A quick, actionable view of how your resume performs against the target role.</p>
        </div>
        <button onClick={onReset} className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 shadow-sm transition hover:border-indigo-200 hover:text-indigo-600">
          <RefreshCw className="h-4 w-4" /> Analyze another
        </button>
      </div>

      <section className="overflow-hidden rounded-2xl bg-slate-900 shadow-xl shadow-slate-200">
        <div className="grid gap-8 p-7 sm:grid-cols-[auto_1fr] sm:items-center sm:p-9">
          <ScoreGauge score={score} />
          <div>
            <div className="flex flex-wrap items-center gap-3">
              <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${status.tone}`}>{status.label}</span>
              {result.has_job_description && <span className="text-xs text-slate-400">Compared with job description</span>}
            </div>
            <h2 className="mt-4 text-2xl font-semibold text-white">You&apos;re on the right track.</h2>
            <p className="mt-2 max-w-xl text-sm leading-6 text-slate-400">
              Your resume has a {score >= 75 ? "solid" : "promising"} foundation. Focus on the priority fixes below to improve your chances of passing an ATS and reaching a recruiter.
            </p>
            <div className="mt-6 grid max-w-lg grid-cols-2 gap-3">
              <div className="rounded-xl border border-slate-700 bg-slate-800/70 px-4 py-3">
                <p className="text-xs text-slate-400">Skills matched</p>
                <p className="mt-1 text-xl font-bold text-white">{matchRate}%</p>
              </div>
              <div className="rounded-xl border border-slate-700 bg-slate-800/70 px-4 py-3">
                <p className="text-xs text-slate-400">Priority actions</p>
                <p className="mt-1 text-xl font-bold text-white">{result.top_improvements.length}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-7">
        <SectionHeading icon={ClipboardCheck} eyebrow="Score breakdown">What makes up your score</SectionHeading>
        <div className="grid gap-x-10 gap-y-6 sm:grid-cols-2">
          <CategoryBar label="ATS compatibility" value={result.category_scores.ats_compatibility} />
          <CategoryBar label="Keyword match" value={result.category_scores.keyword_match} />
          <CategoryBar label="Skills match" value={result.category_scores.skills_match} />
          <CategoryBar label="Formatting" value={result.category_scores.formatting} />
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        {result.top_improvements.length > 0 && (
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-7">
            <SectionHeading icon={Target} eyebrow="Your action plan">Priority fixes</SectionHeading>
            <div className="space-y-3">
              {result.top_improvements.map((imp, i) => (
                <div key={i} className="flex gap-3 rounded-xl border border-slate-100 bg-slate-50 p-3.5">
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-rose-100 text-xs font-bold text-rose-600">{i + 1}</span>
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-500">{imp.category}</span>
                    <p className="mt-0.5 text-sm font-semibold leading-5 text-slate-800">{imp.title}</p>
                  </div>
                  <ArrowUpRight className="ml-auto h-4 w-4 shrink-0 text-slate-300" />
                </div>
              ))}
            </div>
          </section>
        )}

        {result.strengths.length > 0 && (
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-7">
            <SectionHeading icon={CheckCircle2} eyebrow="Keep these">What&apos;s working well</SectionHeading>
            <div className="space-y-3">
              {result.strengths.map((strength, i) => (
                <div key={i} className="flex items-start gap-3 rounded-xl bg-emerald-50/70 p-3.5 text-sm font-medium leading-5 text-emerald-800">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" /> {strength}
                </div>
              ))}
            </div>
          </section>
        )}
      </div>

      {result.has_job_description && (
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-7">
          <SectionHeading icon={AlertCircle} eyebrow="Against the role">Skills match</SectionHeading>
          <div className="flex flex-wrap gap-2">
            {result.matched_skills.map((skill) => <span key={skill} className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700">✓ {skill}</span>)}
            {result.missing_skills.map((skill) => <span key={skill} className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-500">{skill}</span>)}
          </div>
        </section>
      )}

      {result.bullet_rewrites.length > 0 && (
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-7">
          <SectionHeading icon={Sparkles} eyebrow="Make an impact">Rewrite suggestions</SectionHeading>
          <div className="space-y-4">
            {result.bullet_rewrites.map((bullet, i) => (
              <div key={i} className="rounded-xl border border-indigo-100 bg-indigo-50/40 p-4">
                <p className="text-xs leading-5 text-slate-400 line-through">{bullet.original}</p>
                <p className="mt-2 flex items-start gap-2 text-sm font-semibold leading-6 text-slate-800">
                  <Sparkles className="mt-1 h-4 w-4 shrink-0 text-indigo-500" /> {bullet.improved}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
