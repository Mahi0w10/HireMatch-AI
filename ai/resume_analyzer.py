from ai.skill_extractor import compare_skills
from ai.semantic_matcher import calculate_semantic_similarity


def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Analyzes a single resume against a job description.
    Returns matched skills, missing skills, scores, and actionable feedback.
    """
    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not isinstance(job_description, str) or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    result = compare_skills(resume_text, job_description)

    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    has_required_skills = bool(result["required_skills"])

    if has_required_skills:
        explanation = (
            f"Matched {len(result['matched_skills'])} out of "
            f"{len(result['required_skills'])} identified required skills. "
            f"Skill match score: {result['match_score']}%. "
            f"Semantic similarity score: {semantic_score}/100."
        )
    else:
        explanation = (
            "No recognized skills were found in the job description. "
            "A reliable skill match score cannot be calculated. "
            f"Semantic similarity score: {semantic_score}/100."
        )

    suggestions = [
        f"Consider developing your {skill} skills."
        for skill in result["missing_skills"]
    ]

    if not has_required_skills:
        suggestions.insert(
            0,
            "Review the job description and identify its required skills."
        )

    return {
        "skill_match_score": (
            result["match_score"] if has_required_skills else None
        ),
        "semantic_similarity_score": semantic_score,
        "resume_skills": result["resume_skills"],
        "required_skills": result["required_skills"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "explanation": explanation,
        "suggestions": suggestions
    }