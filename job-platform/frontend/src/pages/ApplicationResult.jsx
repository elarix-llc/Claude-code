export default function ApplicationResult({ confirmation, onStartOver }) {
  return (
    <div className="space-y-6">
      {/* Success banner */}
      <div className="card border-emerald-200 bg-gradient-to-br from-emerald-50 to-white text-center py-10">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 text-3xl font-bold">
          &#10003;
        </div>
        <h2 className="mt-4 text-xl font-bold text-slate-900">Application Submitted!</h2>
        <p className="mt-2 text-sm text-slate-500 max-w-sm mx-auto">
          The AI agent applied to <strong>{confirmation.job_title}</strong> at{" "}
          <strong>{confirmation.company}</strong> on your behalf.
        </p>
        <div className="mt-3 inline-flex items-center gap-2 rounded-full bg-slate-100 px-4 py-1.5 text-xs text-slate-600">
          Reference ID: <span className="font-mono font-bold">{confirmation.application_id}</span>
        </div>
      </div>

      {/* Agent steps */}
      <div className="card">
        <h3 className="text-sm font-bold text-slate-900 mb-3">What the agent did</h3>
        <ol className="space-y-2">
          {confirmation.agent_steps.map((step, i) => (
            <li key={i} className="flex items-start gap-3 text-sm text-slate-600">
              <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-brand-100 text-brand-700 text-xs font-bold mt-0.5">
                {i + 1}
              </span>
              {step}
            </li>
          ))}
        </ol>
      </div>

      {/* Cover letter preview */}
      <div className="card">
        <h3 className="text-sm font-bold text-slate-900 mb-2">Cover letter (preview)</h3>
        <p className="text-sm text-slate-600 italic leading-relaxed whitespace-pre-line">
          {confirmation.cover_letter_preview}
        </p>
      </div>

      {/* Privacy note */}
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
        <strong>Privacy notice:</strong> {confirmation.note}
      </div>

      <div className="flex justify-center">
        <button onClick={onStartOver} className="btn-primary">
          Start a new search
        </button>
      </div>
    </div>
  );
}
