"""
Job Matcher Service
Matches candidate profiles to job listings.

LinkedIn's public API does not allow automated job scraping.
This service uses a realistic mock job pool that mirrors LinkedIn Jobs data
structure. The architecture is designed so the mock can be replaced with
a real LinkedIn Jobs API integration (via official partner access) by
swapping out `_fetch_linkedin_jobs()`.
"""

import random
from typing import Optional


# ---------------------------------------------------------------------------
# Mock job database — realistic LinkedIn-style listings
# ---------------------------------------------------------------------------

_JOB_POOL = [
    # Tech / Engineering
    {
        "id": "LI-001",
        "title": "Junior Python Developer",
        "company": "TechStart GmbH",
        "location": "Berlin, Germany",
        "country": "Germany",
        "remote": "Hybrid",
        "description": "Build backend APIs with Python and FastAPI. No prior professional experience required — we train motivated graduates.",
        "requirements": ["python", "sql", "git"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-001",
    },
    {
        "id": "LI-002",
        "title": "Frontend Developer (React)",
        "company": "PixelFlow Ltd.",
        "location": "London, UK",
        "country": "UK",
        "remote": "Remote",
        "description": "Create engaging user interfaces for our SaaS product. Ideal for self-taught developers or recent bootcamp graduates.",
        "requirements": ["react", "javascript", "css", "html"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-002",
    },
    {
        "id": "LI-003",
        "title": "Data Analyst",
        "company": "Insight Analytics",
        "location": "Amsterdam, Netherlands",
        "country": "Netherlands",
        "remote": "On-site",
        "description": "Analyze business data and create dashboards. Excel and SQL skills are essential; Python a plus.",
        "requirements": ["excel", "sql", "data analysis", "tableau"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-003",
    },
    {
        "id": "LI-004",
        "title": "DevOps Engineer",
        "company": "CloudScale Inc.",
        "location": "Toronto, Canada",
        "country": "Canada",
        "remote": "Remote",
        "description": "Manage CI/CD pipelines and cloud infrastructure on AWS. Entry-level candidates with cloud certifications welcome.",
        "requirements": ["aws", "docker", "ci/cd", "linux", "git"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-004",
    },
    {
        "id": "LI-005",
        "title": "UX/UI Designer",
        "company": "DesignHub",
        "location": "New York, USA",
        "country": "USA",
        "remote": "Hybrid",
        "description": "Design intuitive digital products. Strong portfolio required; Figma proficiency essential.",
        "requirements": ["figma", "ux", "ui"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-005",
    },
    {
        "id": "LI-006",
        "title": "Marketing Coordinator",
        "company": "GrowthLab",
        "location": "Dubai, UAE",
        "country": "UAE",
        "remote": "On-site",
        "description": "Support digital marketing campaigns across SEO, email, and social channels.",
        "requirements": ["seo", "email marketing", "social media", "content marketing"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-006",
    },
    {
        "id": "LI-007",
        "title": "Machine Learning Engineer",
        "company": "NeuralWorks",
        "location": "San Francisco, USA",
        "country": "USA",
        "remote": "Hybrid",
        "description": "Train and deploy ML models. Python, TensorFlow or PyTorch required.",
        "requirements": ["machine learning", "python", "tensorflow", "pytorch", "numpy"],
        "level": "mid",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-007",
    },
    {
        "id": "LI-008",
        "title": "Full-Stack Developer",
        "company": "AgileApps",
        "location": "Warsaw, Poland",
        "country": "Poland",
        "remote": "Remote",
        "description": "Build web apps end-to-end with React and Django. Open to junior profiles with personal projects.",
        "requirements": ["react", "python", "django", "sql", "javascript"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-008",
    },
    {
        "id": "LI-009",
        "title": "Java Backend Developer",
        "company": "FinTech Solutions",
        "location": "Singapore",
        "country": "Singapore",
        "remote": "On-site",
        "description": "Develop high-performance financial APIs using Java and Spring Boot.",
        "requirements": ["java", "spring", "sql", "git"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-009",
    },
    {
        "id": "LI-010",
        "title": "Cloud Solutions Architect",
        "company": "SkyEdge",
        "location": "Sydney, Australia",
        "country": "Australia",
        "remote": "Hybrid",
        "description": "Design and implement cloud architectures on Azure and AWS.",
        "requirements": ["aws", "azure", "kubernetes", "terraform", "docker"],
        "level": "mid",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-010",
    },
    {
        "id": "LI-011",
        "title": "Content Writer & SEO Specialist",
        "company": "ContentForge",
        "location": "Remote",
        "country": "Any",
        "remote": "Remote",
        "description": "Write SEO-optimised articles and manage keyword strategy.",
        "requirements": ["seo", "content marketing"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-011",
    },
    {
        "id": "LI-012",
        "title": "Project Manager (Tech)",
        "company": "OrbitSoft",
        "location": "Barcelona, Spain",
        "country": "Spain",
        "remote": "Hybrid",
        "description": "Coordinate cross-functional engineering teams using Agile/Scrum methodology.",
        "requirements": ["agile", "scrum", "project management", "leadership"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-012",
    },
    {
        "id": "LI-013",
        "title": "TypeScript / Node.js Developer",
        "company": "StreamAPI",
        "location": "Dublin, Ireland",
        "country": "Ireland",
        "remote": "Remote",
        "description": "Build real-time APIs and microservices with TypeScript and Node.js.",
        "requirements": ["typescript", "node", "javascript", "sql"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-013",
    },
    {
        "id": "LI-014",
        "title": "Data Scientist",
        "company": "PredictIQ",
        "location": "Paris, France",
        "country": "France",
        "remote": "Hybrid",
        "description": "Apply statistical models and ML to business forecasting problems.",
        "requirements": ["python", "machine learning", "scikit-learn", "pandas", "numpy", "sql"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-014",
    },
    {
        "id": "LI-015",
        "title": "Salesforce Administrator",
        "company": "CRMPro",
        "location": "Chicago, USA",
        "country": "USA",
        "remote": "On-site",
        "description": "Administer and customise Salesforce for enterprise sales teams.",
        "requirements": ["salesforce", "crm"],
        "level": "entry",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs/view/LI-015",
    },
]


# ---------------------------------------------------------------------------
# Matching logic
# ---------------------------------------------------------------------------

def _score_job(job: dict, candidate_skills: list[str], desired_title: str, country: str) -> float:
    """
    Score a job listing against a candidate profile.
    Returns a float 0.0 – 1.0.
    """
    score = 0.0
    max_score = 0.0

    # Skill overlap (60% weight)
    if job["requirements"]:
        max_score += 0.6
        candidate_set = {s.lower() for s in candidate_skills}
        job_set = {r.lower() for r in job["requirements"]}
        overlap = len(candidate_set & job_set)
        skill_score = min(overlap / len(job_set), 1.0) * 0.6
        score += skill_score

    # Title relevance (25% weight)
    max_score += 0.25
    if desired_title:
        title_words = set(desired_title.lower().split())
        job_title_words = set(job["title"].lower().split())
        if title_words & job_title_words:
            score += 0.25
        elif any(w in job["title"].lower() for w in title_words):
            score += 0.12

    # Country / remote preference (15% weight)
    max_score += 0.15
    if country and job["country"].lower() in (country.lower(), "any"):
        score += 0.15
    elif job["remote"] == "Remote":
        score += 0.10

    return round(score / max_score, 3) if max_score > 0 else 0.0


def match_jobs(
    candidate_skills: list[str],
    desired_title: str,
    country: str,
    top_n: int = 10,
) -> list[dict]:
    """
    Search and rank jobs from the pool against the candidate profile.
    Returns the top_n matches with scores, sorted descending.
    """
    scored = []
    for job in _JOB_POOL:
        score = _score_job(job, candidate_skills, desired_title, country)
        if score > 0:
            scored.append({**job, "match_score": score})

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:top_n]


def get_all_jobs() -> list[dict]:
    """Return the full job pool (for testing)."""
    return list(_JOB_POOL)


def get_job_by_id(job_id: str) -> Optional[dict]:
    """Look up a single job by ID."""
    for job in _JOB_POOL:
        if job["id"] == job_id:
            return job
    return None
