"""
Application Agent Service
Simulates an AI agent submitting job applications on behalf of the candidate.

In a production deployment this service would:
  1. Authenticate with LinkedIn via OAuth on the candidate's behalf.
  2. Fill the Easy Apply form programmatically.
  3. Attach the CV and cover letter.
  4. Submit and capture the confirmation.

For this implementation the agent builds a structured application payload,
logs the submission, and returns a confirmation — without persisting any data.
"""

import uuid
from datetime import datetime, timezone


def _build_cover_letter(candidate: dict, job: dict) -> str:
    """Generate a personalised cover letter from candidate + job data."""
    skills_str = ", ".join(candidate.get("skills", [])[:5]) or "various relevant skills"
    return (
        f"Dear Hiring Team at {job['company']},\n\n"
        f"I am writing to express my interest in the {job['title']} role. "
        f"As a {candidate['title']} based in {candidate['country']}, I bring "
        f"hands-on experience with {skills_str}. "
        f"I am excited by the opportunity to contribute to {job['company']} "
        f"and am confident that my background aligns well with your requirements.\n\n"
        f"I look forward to discussing how I can add value to your team.\n\n"
        f"Kind regards,\n{candidate['full_name']}"
    )


def submit_application(candidate: dict, job: dict) -> dict:
    """
    Submit a job application on behalf of the candidate.

    Parameters
    ----------
    candidate : dict
        Ephemeral candidate profile (full_name, email, phone, title, country, skills).
    job : dict
        Job listing dict from the job pool.

    Returns
    -------
    dict
        Confirmation payload. No data is stored after this call returns.
    """
    application_id = str(uuid.uuid4())[:8].upper()
    cover_letter = _build_cover_letter(candidate, job)

    # Simulate the agent actions (would be real API/browser calls in production)
    agent_steps = [
        f"Navigated to {job['apply_url']}",
        f"Filled 'Full Name' with '{candidate['full_name']}'",
        f"Filled 'Email' with '{candidate['email']}'",
        f"Filled 'Phone' with '{candidate['phone']}'",
        "Attached CV document",
        "Pasted generated cover letter",
        "Confirmed application submission",
    ]

    return {
        "application_id": application_id,
        "status": "submitted",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "job_id": job["id"],
        "job_title": job["title"],
        "company": job["company"],
        "cover_letter_preview": cover_letter[:300] + "...",
        "agent_steps": agent_steps,
        "note": "All candidate data will be discarded after this response.",
    }
