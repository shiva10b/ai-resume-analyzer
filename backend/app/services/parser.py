"""
Resume Parsing Service
Extracts raw text from PDF/DOCX resumes and splits into rough sections.
"""
import re
import pdfplumber
import docx
from io import BytesIO


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract raw text from a PDF or DOCX file given as bytes."""
    if filename.lower().endswith(".pdf"):
        return _extract_pdf_text(file_bytes)
    elif filename.lower().endswith(".docx"):
        return _extract_docx_text(file_bytes)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")


def _extract_pdf_text(file_bytes: bytes) -> str:
    text_chunks = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return _clean_text("\n".join(text_chunks))


def _extract_docx_text(file_bytes: bytes) -> str:
    document = docx.Document(BytesIO(file_bytes))
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return _clean_text("\n".join(paragraphs))


def _clean_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


SECTION_HEADERS = [
    "experience", "work experience", "employment",
    "education", "skills", "technical skills",
    "projects", "certifications", "summary", "objective",
]


def split_into_sections(text: str) -> dict:
    """
    Naive section splitter: looks for lines that match common resume
    headers and buckets subsequent lines under them.
    """
    lines = text.split("\n")
    sections = {"header": []}
    current_section = "header"

    for line in lines:
        stripped = line.strip().lower()
        matched_header = next(
            (h for h in SECTION_HEADERS if stripped == h or stripped.startswith(h)),
            None,
        )
        if matched_header:
            current_section = matched_header
            sections.setdefault(current_section, [])
            continue
        sections.setdefault(current_section, []).append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}
