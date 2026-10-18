"""
ATS Scoring Engine
Combines keyword overlap + semantic similarity into a single 0-100 score,
plus a handful of formatting checks that commonly break real ATS parsers.
"""
import os
import re

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:  # pragma: no cover - handled at runtime
    SentenceTransformer = None
    util = None

_model = None


def _get_model():
    global _model
    if SentenceTransformer is None or util is None:
        return None
    if _model is not None:
        return _model

    if os.environ.get("USE_SEMANTIC_SCORING", "").lower() not in {"1", "true", "yes"}:
        return None

    try:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        _model = None
    return _model


def keyword_overlap_score(resume_skills: list[str], jd_skills: list[str]) -> float:
    if not jd_skills:
        return 100.0
    matched = set(resume_skills) & set(jd_skills)
    return round((len(matched) / len(jd_skills)) * 100, 1)


def _lexical_similarity(resume_text: str, jd_text: str) -> float:
    resume_tokens = set(re.findall(r"[a-z0-9]+", resume_text.lower()))
    jd_tokens = set(re.findall(r"[a-z0-9]+", jd_text.lower()))
    if not resume_tokens or not jd_tokens:
        return 0.0
    overlap = resume_tokens & jd_tokens
    union = resume_tokens | jd_tokens
    return round((len(overlap) / len(union)) * 100, 1) if union else 0.0


def semantic_similarity_score(resume_text: str, jd_text: str) -> float:
    model = _get_model()
    if model is None or util is None:
        return _lexical_similarity(resume_text, jd_text)

    try:
        embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)
        similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    except Exception:
        return _lexical_similarity(resume_text, jd_text)

    # cosine similarity is -1..1, clamp and rescale to 0..100
    return round(max(0.0, similarity) * 100, 1)


def formatting_check(resume_text: str) -> list[str]:
    """Flag common ATS-breaking issues. Returns a list of warning strings."""
    warnings = []
    word_count = len(resume_text.split())

    if word_count < 150:
        warnings.append("Resume seems very short — ATS and recruiters may read it as incomplete.")
    if word_count > 1200:
        warnings.append("Resume is long — consider trimming to 1 page for most roles.")
    if not re.search(r"\b(19|20)\d{2}\b", resume_text):
        warnings.append("No dates detected — make sure work/education dates are plain text, not images.")
    if resume_text.count("\t") > 20:
        warnings.append("Heavy use of tabs/tables detected — these can confuse ATS parsers.")
    if not re.search(r"[@]", resume_text):
        warnings.append("No email address detected in the resume text.")

    return warnings


def compute_ats_score(resume_text: str, jd_text: str, resume_skills: list[str], jd_skills: list[str]) -> dict:
    kw_score = keyword_overlap_score(resume_skills, jd_skills)
    sem_score = semantic_similarity_score(resume_text, jd_text)
    final_score = round(0.5 * kw_score + 0.5 * sem_score, 1)

    return {
        "final_score": final_score,
        "keyword_score": kw_score,
        "semantic_score": sem_score,
        "warnings": formatting_check(resume_text),
    }
