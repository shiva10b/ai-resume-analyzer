from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services import parser, nlp_service, scoring, llm_service
from app.schemas.analysis import AnalysisResponse, CategoryScores

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    file_bytes = await resume.read()
    try:
        resume_text = parser.extract_text(file_bytes, resume.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the uploaded file.")

    skill_comparison = nlp_service.compare_skills(resume_text, job_description)
    ats_result = scoring.compute_ats_score(
        resume_text,
        job_description,
        nlp_service.extract_skills(resume_text),
        nlp_service.extract_skills(job_description),
    )

    suggestions = llm_service.generate_suggestions(
        resume_text=resume_text,
        jd_text=job_description,
        score=ats_result["final_score"],
        matched_skills=skill_comparison["matched_skills"],
        missing_skills=skill_comparison["missing_skills"],
    )

    matched_count = len(skill_comparison["matched_skills"])
    total_jd_skills = matched_count + len(skill_comparison["missing_skills"])
    skills_match = round((matched_count / total_jd_skills) * 100, 1) if total_jd_skills else 100.0
    formatting_score = round(max(0, 100 - len(ats_result["warnings"]) * 15), 1)

    category_scores = CategoryScores(
        ats_compatibility=ats_result["final_score"],
        keyword_match=ats_result["keyword_score"],
        skills_match=skills_match,
        formatting=formatting_score,
    )

    return AnalysisResponse(
        final_score=ats_result["final_score"],
        category_scores=category_scores,
        matched_skills=skill_comparison["matched_skills"],
        missing_skills=skill_comparison["missing_skills"],
        strengths=suggestions.get("strengths", []),
        top_improvements=suggestions.get("top_improvements", []),
        bullet_rewrites=suggestions.get("bullet_rewrites", []),
        has_job_description=bool(job_description.strip()),
    )
