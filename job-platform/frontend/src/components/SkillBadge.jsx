export default function SkillBadge({ skill, matched = false }) {
  return (
    <span
      className={[
        "badge text-xs",
        matched
          ? "bg-brand-50 text-brand-700 border border-brand-200"
          : "bg-slate-100 text-slate-600",
      ].join(" ")}
    >
      {skill}
    </span>
  );
}
