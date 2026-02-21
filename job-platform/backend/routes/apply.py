"""
Apply Route
Instructs the AI agent to submit a job application on behalf of the candidate.
No candidate data is persisted after the response is sent.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.application_agent import submit_application
from services.job_matcher import get_job_by_id

router = APIRouter()


class ApplyRequest(BaseModel):
    job_id: str
    full_name: str
    email: str
    phone: str
    title: str
    country: str
    skills: list[str]


class ApplicationConfirmation(BaseModel):
    application_id: str
    status: str
    timestamp: str
    job_id: str
    job_title: str
    company: str
    cover_letter_preview: str
    agent_steps: list[str]
    note: str


@router.post("/submit", response_model=ApplicationConfirmation)
async def apply_to_job(request: ApplyRequest):
    """
    Have the AI agent apply to a job on the candidate's behalf.
    Returns a confirmation. Candidate data is discarded after this call.
    """
    job = get_job_by_id(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{request.job_id}' not found.")

    candidate = {
        "full_name": request.full_name,
        "email": request.email,
        "phone": request.phone,
        "title": request.title,
        "country": request.country,
        "skills": request.skills,
    }

    confirmation = submit_application(candidate, job)
    return confirmation
