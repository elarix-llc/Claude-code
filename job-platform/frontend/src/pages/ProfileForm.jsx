import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import toast from "react-hot-toast";

const COUNTRIES = [
  "Afghanistan","Albania","Algeria","Argentina","Australia","Austria","Bangladesh",
  "Belgium","Brazil","Canada","Chile","China","Colombia","Croatia","Czech Republic",
  "Denmark","Egypt","Ethiopia","Finland","France","Germany","Ghana","Greece","Hungary",
  "India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Japan","Jordan","Kenya",
  "Malaysia","Mexico","Morocco","Netherlands","New Zealand","Nigeria","Norway","Pakistan",
  "Peru","Philippines","Poland","Portugal","Romania","Russia","Saudi Arabia","Singapore",
  "South Africa","South Korea","Spain","Sweden","Switzerland","Taiwan","Thailand","Turkey",
  "UAE","UK","Ukraine","USA","Vietnam","Any / Remote",
];

export default function ProfileForm({ onComplete }) {
  const [fields, setFields] = useState({
    full_name: "",
    email: "",
    phone: "",
    title: "",
    country: "",
  });
  const [cvFile, setCvFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const onDrop = useCallback((accepted) => {
    if (accepted.length > 0) setCvFile(accepted[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"], "text/plain": [".txt"] },
    maxFiles: 1,
    maxSize: 5 * 1024 * 1024,
  });

  function validate() {
    const errs = {};
    if (!fields.full_name.trim()) errs.full_name = "Required";
    if (!fields.email.trim() || !/^\S+@\S+\.\S+$/.test(fields.email))
      errs.email = "Valid email required";
    if (!fields.phone.trim()) errs.phone = "Required";
    if (!fields.title.trim()) errs.title = "Required";
    if (!fields.country) errs.country = "Required";
    if (!cvFile) errs.cv = "Please upload your CV";
    return errs;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    setLoading(true);
    const toastId = toast.loading("Parsing your CV and finding matches...");
    try {
      const formData = new FormData();
      Object.entries(fields).forEach(([k, v]) => formData.append(k, v));
      formData.append("cv", cvFile);

      const { data: profile } = await axios.post("/api/profile/parse", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { data: jobs } = await axios.post("/api/jobs/search", {
        skills: profile.skills,
        title: profile.title,
        country: profile.country,
        top_n: 10,
      });

      toast.success(`Found ${jobs.length} matching roles!`, { id: toastId });
      onComplete(profile, jobs);
    } catch (err) {
      const msg = err.response?.data?.detail || "Something went wrong. Please try again.";
      toast.error(msg, { id: toastId });
    } finally {
      setLoading(false);
    }
  }

  function set(key, value) {
    setFields((prev) => ({ ...prev, [key]: value }));
    if (errors[key]) setErrors((prev) => ({ ...prev, [key]: undefined }));
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div className="card">
        <h2 className="text-lg font-bold text-slate-900">Tell us about yourself</h2>
        <p className="mt-1 text-sm text-slate-500">
          Fill in your details and upload your CV. Our AI agent will scan live job listings
          and match you to the best opportunities.
        </p>

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {/* Full Name */}
          <div className="sm:col-span-2">
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Full Name <span className="text-red-500">*</span>
            </label>
            <input
              className={`input-field ${errors.full_name ? "border-red-400 focus:ring-red-200" : ""}`}
              placeholder="e.g. Alex Johnson"
              value={fields.full_name}
              onChange={(e) => set("full_name", e.target.value)}
            />
            {errors.full_name && <p className="mt-1 text-xs text-red-500">{errors.full_name}</p>}
          </div>

          {/* Email */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Email Address <span className="text-red-500">*</span>
            </label>
            <input
              type="email"
              className={`input-field ${errors.email ? "border-red-400 focus:ring-red-200" : ""}`}
              placeholder="alex@example.com"
              value={fields.email}
              onChange={(e) => set("email", e.target.value)}
            />
            {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email}</p>}
          </div>

          {/* Phone */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Phone Number <span className="text-red-500">*</span>
            </label>
            <input
              type="tel"
              className={`input-field ${errors.phone ? "border-red-400 focus:ring-red-200" : ""}`}
              placeholder="+1 555 123 4567"
              value={fields.phone}
              onChange={(e) => set("phone", e.target.value)}
            />
            {errors.phone && <p className="mt-1 text-xs text-red-500">{errors.phone}</p>}
          </div>

          {/* Desired Title */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Desired Job Title <span className="text-red-500">*</span>
            </label>
            <input
              className={`input-field ${errors.title ? "border-red-400 focus:ring-red-200" : ""}`}
              placeholder="e.g. Frontend Developer"
              value={fields.title}
              onChange={(e) => set("title", e.target.value)}
            />
            {errors.title && <p className="mt-1 text-xs text-red-500">{errors.title}</p>}
          </div>

          {/* Country */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Country <span className="text-red-500">*</span>
            </label>
            <select
              className={`input-field ${errors.country ? "border-red-400 focus:ring-red-200" : ""}`}
              value={fields.country}
              onChange={(e) => set("country", e.target.value)}
            >
              <option value="">Select country...</option>
              {COUNTRIES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
            {errors.country && <p className="mt-1 text-xs text-red-500">{errors.country}</p>}
          </div>

          {/* CV Upload */}
          <div className="sm:col-span-2">
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Upload CV (PDF or TXT, max 5 MB) <span className="text-red-500">*</span>
            </label>
            <div
              {...getRootProps()}
              className={[
                "flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-8 transition",
                isDragActive
                  ? "border-brand-500 bg-brand-50"
                  : cvFile
                  ? "border-emerald-400 bg-emerald-50"
                  : errors.cv
                  ? "border-red-400 bg-red-50"
                  : "border-slate-200 bg-slate-50 hover:border-brand-400 hover:bg-brand-50",
              ].join(" ")}
            >
              <input {...getInputProps()} />
              {cvFile ? (
                <>
                  <div className="text-emerald-600 text-2xl">&#10003;</div>
                  <p className="mt-1 text-sm font-medium text-emerald-700">{cvFile.name}</p>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {(cvFile.size / 1024).toFixed(0)} KB — click or drag to replace
                  </p>
                </>
              ) : (
                <>
                  <svg className="h-10 w-10 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                      d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <p className="mt-2 text-sm text-slate-600">
                    {isDragActive ? "Drop your CV here" : "Drag & drop your CV, or click to browse"}
                  </p>
                  <p className="text-xs text-slate-400 mt-1">PDF or plain text</p>
                </>
              )}
            </div>
            {errors.cv && <p className="mt-1 text-xs text-red-500">{errors.cv}</p>}
          </div>
        </div>

        <div className="mt-6 flex items-center justify-between">
          <p className="text-xs text-slate-400">
            Your information is never stored after this session.
          </p>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? (
              <>
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Scanning jobs...
              </>
            ) : (
              "Find My Jobs"
            )}
          </button>
        </div>
      </div>
    </form>
  );
}
