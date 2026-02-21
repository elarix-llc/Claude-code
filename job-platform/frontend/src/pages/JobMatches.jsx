import { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import JobCard from "../components/JobCard.jsx";
import SkillBadge from "../components/SkillBadge.jsx";

export default function JobMatches({ profile, jobs, onApplied, onBack }) {
  const [applyingId, setApplyingId] = useState(null);

  async function handleApply(job) {
    setApplyingId(job.id);
    const toastId = toast.loading(`Applying to ${job.title} at ${job.company}...`);
    try {
      const { data } = await axios.post("/api/apply/submit", {
        job_id: job.id,
        full_name: profile.full_name,
        email: profile.email,
        phone: profile.phone,
        title: profile.title,
        country: profile.country,
        skills: profile.skills,
      });
      toast.success("Application submitted by the agent!", { id: toastId });
      onApplied(data);
    } catch (err) {
      const msg = err.response?.data?.detail || "Application failed. Please try again.";
      toast.error(msg, { id: toastId });
    } finally {
      setApplyingId(null);
    }
  }

  return (
    <div className="space-y-6">
      {/* Profile summary */}
      <div className="card bg-gradient-to-br from-brand-50 to-white border-brand-100">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="font-bold text-slate-900">{profile.full_name}</h2>
            <p className="text-sm text-slate-500 mt-0.5">
              {profile.title} &middot; {profile.country}
            </p>
          </div>
          <button onClick={onBack} className="btn-secondary text-xs px-3 py-1.5">
            &#8592; Edit profile
          </button>
        </div>

        {profile.skills.length > 0 && (
          <div className="mt-3">
            <p className="text-xs font-semibold text-slate-600 mb-1.5">Skills extracted from CV</p>
            <div className="flex flex-wrap gap-1">
              {profile.skills.map((s) => (
                <SkillBadge key={s} skill={s} matched />
              ))}
            </div>
          </div>
        )}

        {profile.education.length > 0 && (
          <p className="mt-2 text-xs text-slate-500">
            Education: {profile.education.join(", ")}
          </p>
        )}
      </div>

      {/* Results header */}
      <div>
        <h2 className="text-lg font-bold text-slate-900">
          {jobs.length} matching opportunities
        </h2>
        <p className="text-sm text-slate-500 mt-0.5">
          Ranked by how well each role fits your profile. Click &ldquo;Apply via Agent&rdquo; to
          have the AI apply on your behalf.
        </p>
      </div>

      {/* Job cards */}
      {jobs.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-slate-500">No matches found. Try editing your profile or title.</p>
          <button onClick={onBack} className="btn-secondary mt-4">
            Edit profile
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {jobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              candidateSkills={profile.skills}
              onApply={handleApply}
              applying={applyingId === job.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}
