"""
resume_parser.py
Handles extraction of text from PDF and DOCX resumes,
then extracts structured sections (skills, education, experience).
"""

import re
import fitz  # PyMuPDF
from docx import Document


# ──────────────────────────────────────────────────────────────
# 1. RAW TEXT EXTRACTION
# ──────────────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file given its raw bytes."""
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract all text from a DOCX file given its raw bytes."""
    import io
    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs).strip()


def extract_text(uploaded_file) -> str:
    """
    Auto-detect file type and extract text.
    Works with Streamlit UploadedFile objects.
    """
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file type. Please upload PDF or DOCX.")


# ──────────────────────────────────────────────────────────────
# 2. SECTION DETECTION
# ──────────────────────────────────────────────────────────────

SECTION_PATTERNS = {
    "contact":    r"(contact|email|phone|linkedin|github|address)",
    "summary":    r"(summary|objective|profile|about me|career objective)",
    "skills":     r"(skills|technical skills|core competencies|technologies|tools)",
    "experience": r"(experience|work history|employment|internship|projects?)",
    "education":  r"(education|academic|qualification|degree|university|college)",
    "certifications": r"(certif|courses?|training|achievement|award)",
}


def detect_sections(text: str) -> dict:
    """
    Split resume text into named sections using header detection.
    Returns a dict: {section_name: section_text}
    """
    lines = text.split("\n")
    sections = {k: [] for k in SECTION_PATTERNS}
    sections["other"] = []
    current = "other"

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        matched = False
        for section, pattern in SECTION_PATTERNS.items():
            if re.search(pattern, stripped, re.IGNORECASE) and len(stripped) < 60:
                current = section
                matched = True
                break

        if not matched:
            sections[current].append(stripped)

    # Join lines per section
    return {k: " ".join(v) for k, v in sections.items()}


# ──────────────────────────────────────────────────────────────
# 3. CONTACT INFO EXTRACTION
# ──────────────────────────────────────────────────────────────

def extract_contact_info(text: str) -> dict:
    """Extract email, phone, LinkedIn, GitHub from resume text."""
    info = {}

    # Email
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    info["email"] = email_match.group() if email_match else "Not found"

    # Phone
    phone_match = re.search(r"(\+?\d[\d\s\-().]{8,15}\d)", text)
    info["phone"] = phone_match.group().strip() if phone_match else "Not found"

    # LinkedIn
    linkedin_match = re.search(r"linkedin\.com/in/[\w\-]+", text, re.IGNORECASE)
    info["linkedin"] = linkedin_match.group() if linkedin_match else "Not found"

    # GitHub
    github_match = re.search(r"github\.com/[\w\-]+", text, re.IGNORECASE)
    info["github"] = github_match.group() if github_match else "Not found"

    return info


# ──────────────────────────────────────────────────────────────
# 4. SKILLS EXTRACTION
# ──────────────────────────────────────────────────────────────

# Master list of common tech & soft skills to detect
KNOWN_SKILLS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "go", "rust",
    "kotlin", "swift", "r", "scala", "php", "ruby", "bash", "shell",
    # Web
    "html", "css", "react", "angular", "vue", "node.js", "nodejs", "express",
    "django", "flask", "fastapi", "next.js", "tailwind",
    # Data / ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "sklearn",
    "tensorflow", "keras", "pytorch", "opencv", "nltk", "spacy",
    "data analysis", "data science", "data visualization", "statistics",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis", "firebase",
    "oracle", "cassandra", "elasticsearch",
    # Cloud / DevOps
    "aws", "gcp", "azure", "docker", "kubernetes", "git", "github", "gitlab",
    "ci/cd", "jenkins", "terraform", "linux", "unix",
    # Tools
    "tableau", "power bi", "excel", "jupyter", "vs code", "jira", "postman",
    "figma", "photoshop",
    # Soft skills
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "time management", "adaptability", "collaboration",
    "project management", "agile", "scrum",
]


def extract_skills(text: str) -> list:
    """
    Match known skills against resume text (case-insensitive).
    Returns sorted list of found skills.
    """
    text_lower = text.lower()
    found = set()
    for skill in KNOWN_SKILLS:
        # Use word-boundary style matching
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill.title())
    return sorted(found)


# ──────────────────────────────────────────────────────────────
# 5. EDUCATION EXTRACTION
# ──────────────────────────────────────────────────────────────

DEGREE_PATTERNS = [
    r"\b(B\.?Tech|Bachelor of Technology)\b",
    r"\b(B\.?E\.?|Bachelor of Engineering)\b",
    r"\b(B\.?Sc\.?|Bachelor of Science)\b",
    r"\b(B\.?C\.?A\.?|Bachelor of Computer Applications)\b",
    r"\b(M\.?Tech|Master of Technology)\b",
    r"\b(M\.?Sc\.?|Master of Science)\b",
    r"\b(M\.?C\.?A\.?|Master of Computer Applications)\b",
    r"\b(MBA|Master of Business Administration)\b",
    r"\b(Ph\.?D\.?|Doctor of Philosophy)\b",
    r"\b(Diploma)\b",
    r"\b(10th|12th|HSC|SSC|Matriculation)\b",
]

CGPA_PATTERN = r"(CGPA|GPA|Percentage|Score)[:\s]*([0-9.]+\s*%?)"
YEAR_PATTERN  = r"\b(19|20)\d{2}\b"


def extract_education(text: str) -> list:
    """Extract degrees, CGPA, and years from resume text."""
    results = []

    for pattern in DEGREE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            degree = match if isinstance(match, str) else match[0]
            results.append({"degree": degree})

    # Try to add CGPA
    cgpa_match = re.search(CGPA_PATTERN, text, re.IGNORECASE)
    if cgpa_match and results:
        results[0]["cgpa"] = cgpa_match.group(2).strip()

    # Years
    years = re.findall(YEAR_PATTERN, text)
    if years and results:
        results[0]["years"] = years[:2]

    return results if results else [{"degree": "Not detected"}]
