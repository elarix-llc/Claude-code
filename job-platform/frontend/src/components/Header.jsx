export default function Header() {
  return (
    <header className="border-b border-slate-100 bg-white shadow-sm">
      <div className="mx-auto flex max-w-3xl items-center gap-3 px-4 py-4">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-600 text-white font-bold text-lg select-none">
          A
        </div>
        <div>
          <h1 className="text-base font-bold text-slate-900 leading-tight">
            AI Job Match
          </h1>
          <p className="text-xs text-slate-500">
            Find your next role — powered by AI
          </p>
        </div>
        <div className="ml-auto">
          <span className="badge bg-green-50 text-green-700 border border-green-200">
            Privacy-first &bull; No data stored
          </span>
        </div>
      </div>
    </header>
  );
}
