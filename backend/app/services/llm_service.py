"""
LLM Suggestions Service — calls a local Ollama model (free, no API key).
Output is intentionally minimal: a handful of short items, nothing long-form.
"""
import json
import re

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

SYSTEM_PROMPT = """You write extremely short, blunt resume feedback. Titles only,
no explanations, no sentences longer than 8 words. Respond with valid JSON only,
nothing else."""

USER_PROMPT_TEMPLATE = """Resume text:
{resume_text}

Job Description:
{jd_text}

ATS Score: {score}/100
Matched Skills: {matched_skills}
Missing Skills: {missing_skills}

Return JSON with exactly this shape. Every value must be SHORT (under 8 words).

{{
  "strengths": ["short phrase", "short phrase", "short phrase"],
  "top_improvements": [
    {{"category": "Skills", "title": "short issue title, max 6 words"}},
    {{"category": "Experience", "title": "short issue title, max 6 words"}},
    {{"category": "Keywords", "title": "short issue title, max 6 words"}}
  ],
  "bullet_rewrites": [
    {{"original": "an actual weak line from the resume", "improved": "a stronger short rewrite"}},
    {{"original": "another actual weak line from the resume", "improved": "a stronger short rewrite"}}
  ]
}}
"""


def _fallback_suggestions(resume_text: str, jd_text: str, score: float,
                         matched_skills: list[str], missing_skills: list[str]) -> dict:
    strengths = []
    if matched_skills:
        strengths = [f"Strong {skill} fit" for skill in matched_skills[:3]]
    if not strengths:
        strengths = ["Clear role alignment", "Relevant experience"]

    improvements = []
    if missing_skills:
        for skill in missing_skills[:3]:
            improvements.append({"category": "Skills", "title": f"Add {skill}"})
    if not improvements:
        improvements = [{"category": "Experience", "title": "Add quantified results"}]

    resume_lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    candidate_lines = [line for line in resume_lines if len(line) > 20][:3]
    bullet_rewrites = []
    for line in candidate_lines:
        cleaned = re.sub(r"\s+", " ", line).strip()
        if not cleaned:
            continue
        bullet_rewrites.append(
            {
                "original": cleaned[:120],
                "improved": "Improved impact with measurable results and role keywords.",
            }
        )
    if not bullet_rewrites:
        bullet_rewrites.append(
            {
                "original": "Worked on projects and delivered results.",
                "improved": "Delivered measurable impact using core role requirements and tools.",
            }
        )

    return {
        "strengths": strengths[:3],
        "top_improvements": improvements[:3],
        "bullet_rewrites": bullet_rewrites[:3],
    }


def generate_suggestions(resume_text: str, jd_text: str, score: float,
                          matched_skills: list[str], missing_skills: list[str]) -> dict:
    try:
        prompt = USER_PROMPT_TEMPLATE.format(
            resume_text=resume_text[:8000],
            jd_text=jd_text[:4000],
            score=score,
            matched_skills=", ".join(matched_skills) or "none",
            missing_skills=", ".join(missing_skills) or "none",
        )

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "system": SYSTEM_PROMPT,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"num_predict": 700, "temperature": 0.3},
            },
            timeout=12,
        )
        response.raise_for_status()

        raw_text = response.json().get("response", "").strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return _fallback_suggestions(resume_text, jd_text, score, matched_skills, missing_skills)
    except (requests.RequestException, TimeoutError, ValueError):
        return _fallback_suggestions(resume_text, jd_text, score, matched_skills, missing_skills)
