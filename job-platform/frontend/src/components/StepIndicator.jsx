export default function StepIndicator({ steps, current }) {
  return (
    <nav aria-label="Progress">
      <ol className="flex items-center gap-0">
        {steps.map((label, index) => {
          const done = index < current;
          const active = index === current;
          return (
            <li key={label} className="flex flex-1 items-center">
              <div className="flex flex-col items-center gap-1 flex-1">
                <div
                  className={[
                    "flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold transition-all",
                    done
                      ? "bg-brand-600 text-white"
                      : active
                      ? "bg-brand-600 text-white ring-4 ring-brand-100"
                      : "bg-slate-100 text-slate-400",
                  ].join(" ")}
                >
                  {done ? (
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    index + 1
                  )}
                </div>
                <span
                  className={[
                    "text-xs font-medium whitespace-nowrap",
                    active ? "text-brand-600" : done ? "text-slate-600" : "text-slate-400",
                  ].join(" ")}
                >
                  {label}
                </span>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={[
                    "h-0.5 flex-1 mx-2 mb-5 rounded-full transition-all",
                    done ? "bg-brand-600" : "bg-slate-100",
                  ].join(" ")}
                />
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
