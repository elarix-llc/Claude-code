"""
CV Parser Service
Extracts text and key information from uploaded PDF CVs.
All data is processed in-memory; nothing is written to disk.
"""

import io
import re
from typing import Optional

try:
    import pdfplumber
    PDF_BACKEND = "pdfplumber"
except BaseException:
    PDF_BACKEND = None

try:
    import PyPDF2
    PDF_FALLBACK = "PyPDF2"
except BaseException:
    PDF_FALLBACK = None


# Skills taxonomy for extraction
SKILL_KEYWORDS = {
    "programming": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "php", "ruby", "swift", "kotlin", "sql", "html", "css", "bash",
    ],
    "frameworks": [
        "react", "vue", "angular", "django", "flask", "fastapi", "spring",
        "express", "nextjs", "nuxt", "laravel", "rails", "node",
    ],
    "data": [
        "machine learning", "deep learning", "data analysis", "pandas", "numpy",
        "tensorflow", "pytorch", "scikit-learn", "tableau", "power bi", "excel",
        "sql", "nosql", "mongodb", "postgresql",
    ],
    "cloud": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd",
        "devops", "linux", "git",
    ],
    "soft": [
        "leadership", "communication", "teamwork", "agile", "scrum", "project management",
        "problem solving", "analytical", "critical thinking",
    ],
    "design": [
        "figma", "adobe", "ux", "ui", "photoshop", "illustrator", "sketch",
    ],
    "marketing": [
        "seo", "sem", "google ads", "social media", "content marketing",
        "email marketing", "crm", "hubspot", "salesforce",
    ],
}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract raw text from CV bytes. Handles PDF and plain-text files."""
    text = ""

    # Detect plain text files (not PDF magic bytes)
    is_pdf = file_bytes[:4] == b"%PDF"

    if not is_pdf:
        # Plain text or unknown — decode directly
        try:
            return file_bytes.decode("utf-8", errors="ignore").strip()
        except Exception:
            return ""

    if PDF_BACKEND == "pdfplumber":
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            pass

    if not text and PDF_FALLBACK == "PyPDF2":
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception:
            pass

    if not text:
        # Last resort: decode raw bytes
        text = file_bytes.decode("utf-8", errors="ignore")

    return text.strip()


def extract_skills(text: str) -> list[str]:
    """Extract skills from text using keyword matching."""
    text_lower = text.lower()
    found_skills = []
    for category, keywords in SKILL_KEYWORDS.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text_lower):
                found_skills.append(kw)
    return list(dict.fromkeys(found_skills))  # deduplicate, preserve order


def extract_experience_years(text: str) -> Optional[int]:
    """Heuristically estimate years of experience from CV text."""
    patterns = [
        r"(\d+)\+?\s*years?\s+of\s+experience",
        r"(\d+)\+?\s*years?\s+experience",
        r"experience\s+of\s+(\d+)\+?\s*years?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def extract_education(text: str) -> list[str]:
    """Extract education level mentions."""
    degrees = []
    degree_patterns = {
        "PhD": r"\b(ph\.?d|doctor(?:ate)?|d\.phil)\b",
        "Master's": r"\b(master(?:'s)?|m\.?sc?\.?|m\.?eng\.?|m\.?b\.?a\.?)\b",
        "Bachelor's": r"\b(bachelor(?:'s)?|b\.?sc?\.?|b\.?eng\.?|b\.?a\.?|undergraduate)\b",
        "Associate's": r"\b(associate(?:'s)?|a\.?s\.?|a\.?a\.?)\b",
        "High School": r"\b(high school|secondary school|diploma|ged)\b",
    }
    text_lower = text.lower()
    for label, pattern in degree_patterns.items():
        if re.search(pattern, text_lower):
            degrees.append(label)
    return degrees


def parse_cv(file_bytes: bytes, filename: str = "") -> dict:
    """
    Main entry point: parse a CV file and return structured profile data.
    Returns an ephemeral dict; nothing is stored.
    """
    text = extract_text_from_pdf(file_bytes)
    skills = extract_skills(text)
    years_exp = extract_experience_years(text)
    education = extract_education(text)

    return {
        "raw_text_preview": text[:500] if text else "(Could not extract text)",
        "skills": skills,
        "years_experience": years_exp,
        "education": education,
        "word_count": len(text.split()),
    }
