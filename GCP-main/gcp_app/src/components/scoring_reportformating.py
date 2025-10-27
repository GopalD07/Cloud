from typing import List, Dict
from langchain_core.documents import Document

def _score_ats(resume_text: str, jd_text: str) -> int:
    # VERY naive overlap-based score for demo. Replace with your LLM flow if needed.
    resume_terms = set(w.lower() for w in resume_text.split())
    jd_terms = set(w.lower() for w in jd_text.split())
    if not jd_terms:
        return 0
    overlap = len(resume_terms & jd_terms)
    return min(int(100 * overlap / (len(jd_terms) + 1)), 100)

def generate_full_report(resume_chunks: List[Document], jd_text: str) -> Dict[str, str]:
    resume_text = "\n".join([d.page_content for d in resume_chunks])
    ats = _score_ats(resume_text, jd_text)
    swot = f"""
    **Strengths**
    - Relevant keyword overlap with JD.
    - Clear structure and readable formatting.

    **Weaknesses**
    - Missing some specific JD keywords/skills.
    - Limited measurable impact statements.

    **Opportunities**
    - Tailor summary to mirror JD responsibilities.
    - Add metrics for achievements.

    **Threats**
    - Competing candidates with closer domain match.
    - ATS filtering for exact keywords.
    """
    sugg = f"""
    - Add 5–8 exact keywords from the JD into Skills & Experience.
    - Quantify results (e.g., reduced X by Y%).
    - Reorder sections so top 1–2 experiences appear first.
    - Keep to 1–2 pages; use consistent bullet style.
    """
    return {
        "SWOT_Analysis": swot.strip(),
        "ATS_Score": f"**Estimated ATS score:** {ats}/100",
        "Suggestions": sugg.strip()
    }
