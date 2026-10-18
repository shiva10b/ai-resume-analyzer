"""
NLP Service — skill & entity extraction.
Uses a curated skills dictionary matched against lowercased text
(fast, dependency-light) plus spaCy for general entity extraction.
"""
import re

try:
    import spacy
except ImportError:  # pragma: no cover - handled at runtime
    spacy = None

if spacy is not None:
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = spacy.blank("en")
else:
    nlp = None

# Extend this list freely — it's the backbone of the matching quality.
SKILLS_DB = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "sql",
    # Web/Frameworks
    "react", "node.js", "express", "fastapi", "django", "flask", "next.js", "vue",
    # AI/ML
    "machine learning", "deep learning", "nlp", "computer vision", "pytorch",
    "tensorflow", "scikit-learn", "pandas", "numpy", "spacy", "llm", "rag",
    "prompt engineering", "hugging face", "keras",
    # Data/Infra
    "docker", "kubernetes", "aws", "azure", "gcp", "postgresql", "mongodb",
    "redis", "git", "ci/cd", "linux",
    # Soft/General
    "communication", "leadership", "project management", "agile", "problem solving",
]


def extract_skills(text: str) -> list[str]:
    """Return the set of known skills found in the given text."""
    text_lower = text.lower()
    found = set()
    for skill in SKILLS_DB:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text_lower):
            found.add(skill)
    return sorted(found)


def extract_entities(text: str) -> dict:
    """Pull organizations, dates, and other named entities via spaCy."""
    if nlp is None:
        return {"organizations": [], "dates": [], "people": []}

    doc = nlp(text[:100_000])  # guard against extremely long input
    entities = {"organizations": set(), "dates": set(), "people": set()}
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["organizations"].add(ent.text.strip())
        elif ent.label_ == "DATE":
            entities["dates"].add(ent.text.strip())
        elif ent.label_ == "PERSON":
            entities["people"].add(ent.text.strip())
    return {k: sorted(v) for k, v in entities.items()}


def compare_skills(resume_text: str, jd_text: str) -> dict:
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    return {
        "matched_skills": sorted(resume_skills & jd_skills),
        "missing_skills": sorted(jd_skills - resume_skills),
        "extra_skills": sorted(resume_skills - jd_skills),
    }
