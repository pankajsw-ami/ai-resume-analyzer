"""
job_matcher.py
Computes similarity between resume text and job description using:
  - TF-IDF cosine similarity (overall match score)
  - Skill-level keyword matching
  - ATS keyword analysis
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.resume_parser import KNOWN_SKILLS, extract_skills


# ──────────────────────────────────────────────────────────────
# 1. TEXT CLEANING
# ──────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Lowercase, remove special chars, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\+\#]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ──────────────────────────────────────────────────────────────
# 2. OVERALL MATCH SCORE  (TF-IDF cosine similarity)
# ──────────────────────────────────────────────────────────────

def compute_match_score(resume_text: str, job_text: str) -> float:
    """
    Returns a 0–100 similarity score between resume and JD.
    Uses TF-IDF vectors + cosine similarity.
    """
    corpus = [clean_text(resume_text), clean_text(job_text)]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(corpus)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(score) * 100, 2)


# ──────────────────────────────────────────────────────────────
# 3. SKILL GAP ANALYSIS
# ──────────────────────────────────────────────────────────────

def skill_gap_analysis(resume_skills: list, job_text: str) -> dict:
    """
    Compare resume skills vs skills required in the job description.
    Returns:
      matched   – skills you have that the JD wants
      missing   – skills JD wants that you lack
      extra     – skills you have not mentioned in JD (bonus)
    """
    job_text_lower = job_text.lower()

    # Find skills mentioned in JD
    jd_skills = set()
    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, job_text_lower):
            jd_skills.add(skill.title())

    resume_skill_set = set(resume_skills)

    matched = sorted(resume_skill_set & jd_skills)
    missing = sorted(jd_skills - resume_skill_set)
    extra   = sorted(resume_skill_set - jd_skills)

    return {
        "matched": matched,
        "missing": missing,
        "extra":   extra,
        "jd_skills": sorted(jd_skills),
        "skill_match_pct": round(
            len(matched) / len(jd_skills) * 100 if jd_skills else 0, 1
        ),
    }


# ──────────────────────────────────────────────────────────────
# 4. ATS KEYWORD ANALYSIS
# ──────────────────────────────────────────────────────────────

def extract_ats_keywords(job_text: str, top_n: int = 25) -> list:
    """
    Extract the most important ATS keywords from job description
    using TF-IDF on the JD itself (unigrams + bigrams).
    Returns list of (keyword, score) tuples.
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=200,
    )
    tfidf_matrix = vectorizer.fit_transform([clean_text(job_text)])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    keyword_scores = sorted(
        zip(feature_names, scores), key=lambda x: x[1], reverse=True
    )

    # Filter out very short or purely numeric tokens
    filtered = [
        (kw, round(sc, 4))
        for kw, sc in keyword_scores
        if len(kw) > 2 and not kw.isdigit()
    ]
    return filtered[:top_n]


def ats_keyword_hit_rate(resume_text: str, ats_keywords: list) -> dict:
    """
    Check which ATS keywords appear in the resume.
    Returns hit/miss breakdown and overall hit rate %.
    """
    resume_lower = clean_text(resume_text)
    hits, misses = [], []

    for kw, score in ats_keywords:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, resume_lower):
            hits.append(kw)
        else:
            misses.append(kw)

    total = len(ats_keywords)
    return {
        "hits":     hits,
        "misses":   misses,
        "hit_rate": round(len(hits) / total * 100, 1) if total else 0,
    }


# ──────────────────────────────────────────────────────────────
# 5. COMPOSITE SCORE & GRADE
# ──────────────────────────────────────────────────────────────

def compute_composite_score(
    match_score: float,
    skill_match_pct: float,
    ats_hit_rate: float,
) -> dict:
    """
    Weighted composite score:
      40% – overall TF-IDF match
      35% – skill match %
      25% – ATS keyword hit rate
    Returns score (0-100) and letter grade.
    """
    composite = (
        0.40 * match_score +
        0.35 * skill_match_pct +
        0.25 * ats_hit_rate
    )
    composite = round(composite, 1)

    if composite >= 80:
        grade, label = "A", "Excellent Match 🎯"
    elif composite >= 65:
        grade, label = "B", "Good Match ✅"
    elif composite >= 50:
        grade, label = "C", "Moderate Match ⚠️"
    elif composite >= 35:
        grade, label = "D", "Weak Match 📉"
    else:
        grade, label = "F", "Poor Match ❌"

    return {"score": composite, "grade": grade, "label": label}


# ──────────────────────────────────────────────────────────────
# 6. IMPROVEMENT SUGGESTIONS
# ──────────────────────────────────────────────────────────────

SKILL_RESOURCES = {
    "python":          "https://www.learnpython.org",
    "machine learning":"https://www.coursera.org/learn/machine-learning",
    "deep learning":   "https://www.deeplearning.ai",
    "sql":             "https://www.sqlzoo.net",
    "docker":          "https://docs.docker.com/get-started/",
    "aws":             "https://aws.amazon.com/training/",
    "react":           "https://react.dev/learn",
    "git":             "https://learngitbranching.js.org",
    "data analysis":   "https://www.kaggle.com/learn",
    "nlp":             "https://huggingface.co/learn",
}


def generate_suggestions(missing_skills: list, ats_misses: list) -> list:
    """
    Generate actionable improvement suggestions for missing skills.
    """
    suggestions = []

    for skill in missing_skills[:8]:          # top 8 missing skills
        skill_lower = skill.lower()
        resource = SKILL_RESOURCES.get(skill_lower, "https://www.google.com/search?q=learn+" + skill_lower.replace(" ", "+"))
        suggestions.append({
            "skill":    skill,
            "action":   f"Add '{skill}' to your skills section or build a project using it.",
            "resource": resource,
        })

    if ats_misses:
        suggestions.append({
            "skill":    "ATS Keywords",
            "action":   f"Incorporate these missing ATS keywords naturally: {', '.join(ats_misses[:5])}",
            "resource": "https://www.jobscan.co",
        })

    if not suggestions:
        suggestions.append({
            "skill":    "All Good!",
            "action":   "Your resume is well-optimized. Focus on quantifying achievements.",
            "resource": "",
        })

    return suggestions
