from pydantic import BaseModel


class BulletRewrite(BaseModel):
    original: str
    improved: str


class Improvement(BaseModel):
    category: str
    title: str


class CategoryScores(BaseModel):
    ats_compatibility: float
    keyword_match: float
    skills_match: float
    formatting: float


class AnalysisResponse(BaseModel):
    final_score: float
    category_scores: CategoryScores
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    top_improvements: list[Improvement]
    bullet_rewrites: list[BulletRewrite]
    has_job_description: bool
