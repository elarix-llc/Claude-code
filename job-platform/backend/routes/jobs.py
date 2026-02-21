"""
Jobs Route
Searches and ranks job listings against the candidate profile.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from services.job_matcher import match_jobs

router = APIRouter()


class SearchRequest(BaseModel):
    skills: list[str]
    title: str
    country: str
    top_n: int = 10


class JobResult(BaseModel):
    id: str
    title: str
    company: str
    location: str
    country: str
    remote: str
    description: str
    requirements: list[str]
    level: str
    source: str
    apply_url: str
    match_score: float


@router.post("/search", response_model=list[JobResult])
async def search_jobs(request: SearchRequest):
    """
    Match the candidate's profile against available job listings.
    Returns a ranked list of opportunities. No data is stored.
    """
    results = match_jobs(
        candidate_skills=request.skills,
        desired_title=request.title,
        country=request.country,
        top_n=request.top_n,
    )
    return results
