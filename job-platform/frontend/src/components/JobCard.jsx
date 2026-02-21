import SkillBadge from "./SkillBadge.jsx";

const REMOTE_COLOR = {
  Remote: "bg-emerald-50 text-emerald-700 border-emerald-200",
  Hybrid: "bg-yellow-50 text-yellow-700 border-yellow-200",
  "On-site": "bg-slate-100 text-slate-600 border-slate-200",
};

export default function JobCard({ job, candidateSkills, onApply, applying }) {
  const candidateSet = new Set((candidateSkills || []).map((s) => s.toLowerCase()));
  const pct = Math.round(job.match_score * 100);
  const scoreColor =
    pct >= 70 ? "text-emerald-600" : pct >= 40 ? "text-yellow-600" : "text-slate-500";

  return (
    <article className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-900 truncate">{job.title}</h3>
          <p className="text-sm text-slate-500 mt-0.5">
            {job.company} &middot; {job.location}
          </p>
        </div>
        <div className="flex flex-col items-end gap-1 shrink-0">
          <span className={`text-xl font-bold ${scoreColor}`}>{pct}%</span>
          <span className="text-xs text-slate-400">match</span>
        </div>
      </div>

      <div className="mt-3 flex flex-wrap gap-1.5">
        <span className={`badge border ${REMOTE_COLOR[job.remote] || REMOTE_COLOR["On-site"]}`}>
          {job.remote}
        </span>
        <span className="badge bg-slate-100 text-slate-600">{job.level} level</span>
        <span className="badge bg-slate-100 text-slate-600">{job.source}</span>
      </div>

      <p className="mt-3 text-sm text-slate-600 leading-relaxed">{job.description}</p>

      <div className="mt-3 flex flex-wrap gap-1">
        {job.requirements.map((req) => (
          <SkillBadge key={req} skill={req} matched={candidateSet.has(req.toLowerCase())} />
        ))}
      </div>

      <div className="mt-4 flex items-center gap-3">
        <button
          onClick={() => onApply(job)}
          disabled={applying}
          className="btn-primary text-xs px-4 py-2"
        >
          {applying ? (
            <>
              <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Agent applying...
            </>
          ) : (
            "Apply via Agent"
          )}
        </button>
        <a
          href={job.apply_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-brand-600 hover:underline"
        >
          View on {job.source}
        </a>
      </div>
    </article>
  );
}
