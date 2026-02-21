"""
Profile Route
Accepts the candidate form + CV upload, parses the CV, and returns
an ephemeral structured profile ready for job matching.
"""

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr

from services.cv_parser import parse_cv

router = APIRouter()


class ParsedProfile(BaseModel):
    full_name: str
    email: str
    phone: str
    title: str
    country: str
    skills: list[str]
    years_experience: int | None
    education: list[str]
    cv_word_count: int
    cv_preview: str


@router.post("/parse", response_model=ParsedProfile)
async def parse_profile(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    title: str = Form(...),
    country: str = Form(...),
    cv: UploadFile = File(...),
):
    """
    Accept the candidate form and CV file.
    Parse the CV and return a structured, ephemeral profile.
    This data is NOT stored.
    """
    allowed_types = {"application/pdf", "text/plain"}
    if cv.content_type not in allowed_types and not cv.filename.endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF or plain-text CV files are accepted.",
        )

    file_bytes = await cv.read()
    if len(file_bytes) > 5 * 1024 * 1024:  # 5 MB cap
        raise HTTPException(status_code=400, detail="CV file must be under 5 MB.")

    cv_data = parse_cv(file_bytes, cv.filename)

    return ParsedProfile(
        full_name=full_name,
        email=email,
        phone=phone,
        title=title,
        country=country,
        skills=cv_data["skills"],
        years_experience=cv_data["years_experience"],
        education=cv_data["education"],
        cv_word_count=cv_data["word_count"],
        cv_preview=cv_data["raw_text_preview"],
    )
