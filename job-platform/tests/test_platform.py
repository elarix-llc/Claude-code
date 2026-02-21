"""
Integration tests for the AI Job Match Platform.
Sends realistic sample candidate profiles through the full pipeline:
  profile parse → job search → application submission.
"""

import io
import pytest
from httpx import AsyncClient, ASGITransport

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from main import app

# ---------------------------------------------------------------------------
# Sample candidate profiles (realistic, randomised personas)
# ---------------------------------------------------------------------------

SAMPLE_CANDIDATES = [
    {
        "id": "candidate-001",
        "full_name": "Sofia Reyes",
        "email": "sofia.reyes@example.com",
        "phone": "+34 612 345 678",
        "title": "Frontend Developer",
        "country": "Spain",
        "cv_text": (
            "Sofia Reyes — Frontend Developer\n"
            "Skills: React, JavaScript, TypeScript, CSS, HTML, Git\n"
            "Education: Bachelor's in Computer Science, Universidad de Madrid, 2023\n"
            "Projects: Built a personal portfolio site and a React todo app.\n"
            "Languages: Spanish (native), English (C1)"
        ),
        "expected_min_jobs": 1,
    },
    {
        "id": "candidate-002",
        "full_name": "Kwame Asante",
        "email": "kwame.asante@example.com",
        "phone": "+233 20 123 4567",
        "title": "Data Analyst",
        "country": "Ghana",
        "cv_text": (
            "Kwame Asante — Data Analyst\n"
            "Skills: Python, SQL, Excel, Tableau, Data Analysis, Pandas\n"
            "Education: Bachelor's in Statistics, University of Ghana, 2022\n"
            "Experience: Internship analysing sales data with Excel and SQL.\n"
            "Languages: English (native), Twi"
        ),
        "expected_min_jobs": 1,
    },
    {
        "id": "candidate-003",
        "full_name": "Lena Müller",
        "email": "lena.mueller@example.com",
        "phone": "+49 170 9876543",
        "title": "UX Designer",
        "country": "Germany",
        "cv_text": (
            "Lena Müller — UX/UI Designer\n"
            "Skills: Figma, UX, UI, Adobe, Sketch\n"
            "Education: Master's in Interaction Design, TU Berlin, 2023\n"
            "Portfolio: Redesigned mobile banking app — 30% increase in engagement.\n"
            "Languages: German (native), English (B2)"
        ),
        "expected_min_jobs": 1,
    },
    {
        "id": "candidate-004",
        "full_name": "Arjun Patel",
        "email": "arjun.patel@example.com",
        "phone": "+91 98765 43210",
        "title": "Python Developer",
        "country": "India",
        "cv_text": (
            "Arjun Patel — Python Backend Developer\n"
            "Skills: Python, Django, FastAPI, SQL, PostgreSQL, Git, Docker\n"
            "Education: Bachelor's in Information Technology, IIT Bombay, 2024\n"
            "Open-source contributor: 3 PRs merged to Django.\n"
            "Languages: Hindi (native), English (fluent)"
        ),
        "expected_min_jobs": 1,
    },
    {
        "id": "candidate-005",
        "full_name": "Mia Thompson",
        "email": "mia.thompson@example.com",
        "phone": "+1 416 555 0192",
        "title": "Cloud Engineer",
        "country": "Canada",
        "cv_text": (
            "Mia Thompson — Cloud/DevOps Engineer\n"
            "Skills: AWS, Docker, Kubernetes, Linux, CI/CD, Terraform, Git\n"
            "Certifications: AWS Cloud Practitioner (2023)\n"
            "Education: Associate's in Network Systems Technology, Seneca College, 2022\n"
            "Languages: English (native), French (A2)"
        ),
        "expected_min_jobs": 1,
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_cv_file(text: str, filename: str = "cv.txt") -> tuple:
    """Return a tuple suitable for httpx multipart upload."""
    return (filename, io.BytesIO(text.encode("utf-8")), "text/plain")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.mark.asyncio
@pytest.mark.parametrize("candidate", SAMPLE_CANDIDATES, ids=[c["id"] for c in SAMPLE_CANDIDATES])
async def test_full_pipeline(candidate):
    """
    End-to-end test: parse profile → match jobs → submit application.
    Verifies the full agent pipeline for each sample candidate.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:

        # ── Step 1: Parse CV ──────────────────────────────────────────────
        cv_file = make_cv_file(candidate["cv_text"])
        response = await client.post(
            "/api/profile/parse",
            files={"cv": cv_file},
            data={
                "full_name": candidate["full_name"],
                "email": candidate["email"],
                "phone": candidate["phone"],
                "title": candidate["title"],
                "country": candidate["country"],
            },
        )
        assert response.status_code == 200, f"Profile parse failed: {response.text}"
        profile = response.json()

        assert profile["full_name"] == candidate["full_name"]
        assert profile["email"] == candidate["email"]
        assert isinstance(profile["skills"], list)
        assert len(profile["skills"]) > 0, "Expected at least one skill to be extracted"

        # ── Step 2: Search Jobs ───────────────────────────────────────────
        response = await client.post(
            "/api/jobs/search",
            json={
                "skills": profile["skills"],
                "title": profile["title"],
                "country": profile["country"],
                "top_n": 5,
            },
        )
        assert response.status_code == 200, f"Job search failed: {response.text}"
        jobs = response.json()

        assert len(jobs) >= candidate["expected_min_jobs"], (
            f"Expected >= {candidate['expected_min_jobs']} jobs, got {len(jobs)}"
        )
        # Scores should be in descending order
        scores = [j["match_score"] for j in jobs]
        assert scores == sorted(scores, reverse=True), "Jobs not sorted by match score"

        # ── Step 3: Apply via Agent ───────────────────────────────────────
        top_job = jobs[0]
        response = await client.post(
            "/api/apply/submit",
            json={
                "job_id": top_job["id"],
                "full_name": candidate["full_name"],
                "email": candidate["email"],
                "phone": candidate["phone"],
                "title": candidate["title"],
                "country": candidate["country"],
                "skills": profile["skills"],
            },
        )
        assert response.status_code == 200, f"Application failed: {response.text}"
        confirmation = response.json()

        assert confirmation["status"] == "submitted"
        assert confirmation["job_id"] == top_job["id"]
        assert confirmation["company"] == top_job["company"]
        assert len(confirmation["application_id"]) > 0
        assert len(confirmation["agent_steps"]) >= 5
        assert "discarded" in confirmation["note"].lower() or "data" in confirmation["note"].lower()

        print(
            f"\n[{candidate['id']}] {candidate['full_name']} → "
            f"{top_job['title']} at {top_job['company']} "
            f"(score: {top_job['match_score']}) "
            f"[ref: {confirmation['application_id']}]"
        )


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/health")
        assert r.status_code == 200
        assert r.json()["data_persistence"] is False


@pytest.mark.asyncio
async def test_invalid_job_id_returns_404():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/apply/submit",
            json={
                "job_id": "NONEXISTENT",
                "full_name": "Test User",
                "email": "test@test.com",
                "phone": "000",
                "title": "Developer",
                "country": "USA",
                "skills": [],
            },
        )
        assert r.status_code == 404


@pytest.mark.asyncio
async def test_missing_cv_returns_422():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/profile/parse",
            data={
                "full_name": "No CV",
                "email": "nocv@test.com",
                "phone": "000",
                "title": "Dev",
                "country": "UK",
            },
        )
        assert r.status_code == 422
