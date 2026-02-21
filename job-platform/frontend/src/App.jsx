import { useState } from "react";
import ProfileForm from "./pages/ProfileForm.jsx";
import JobMatches from "./pages/JobMatches.jsx";
import ApplicationResult from "./pages/ApplicationResult.jsx";
import Header from "./components/Header.jsx";
import StepIndicator from "./components/StepIndicator.jsx";

const STEPS = ["Your Profile", "Job Matches", "Application Sent"];

export default function App() {
  const [step, setStep] = useState(0);
  const [profile, setProfile] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [confirmation, setConfirmation] = useState(null);

  function handleProfileParsed(parsedProfile, matchedJobs) {
    setProfile(parsedProfile);
    setJobs(matchedJobs);
    setStep(1);
  }

  function handleApplied(confirmationData) {
    setConfirmation(confirmationData);
    setStep(2);
  }

  function handleStartOver() {
    setStep(0);
    setProfile(null);
    setJobs([]);
    setConfirmation(null);
  }

  return (
    <div className="min-h-screen">
      <Header />
      <main className="mx-auto max-w-3xl px-4 py-10">
        <StepIndicator steps={STEPS} current={step} />
        <div className="mt-8">
          {step === 0 && <ProfileForm onComplete={handleProfileParsed} />}
          {step === 1 && (
            <JobMatches
              profile={profile}
              jobs={jobs}
              onApplied={handleApplied}
              onBack={() => setStep(0)}
            />
          )}
          {step === 2 && (
            <ApplicationResult
              confirmation={confirmation}
              onStartOver={handleStartOver}
            />
          )}
        </div>
      </main>

      <footer className="mt-16 border-t border-slate-100 py-6 text-center text-xs text-slate-400">
        AI Job Match Platform &mdash; Your data is never stored after this session ends.
      </footer>
    </div>
  );
}
