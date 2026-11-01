from ai.skill_extractor import compare_skills
from ai.semantic_matcher import calculate_semantic_similarity


def analyze_resume(resume_text, job_description):
    result = compare_skills(resume_text, job_description)
    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    analysis = {
        "skill_match_score": result["match_score"],
        "semantic_similarity_score": semantic_score,
        "resume_skills": result["resume_skills"],
        "required_skills": result["required_skills"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "explanation": (
            f"Matched {len(result['matched_skills'])} out of "
            f"{len(result['required_skills'])} identified required skills. "
            f"Semantic similarity score: {semantic_score}/100."
        ),
        "suggestions": [
            f"Consider developing your {skill} skills."
            for skill in result["missing_skills"]
        ]
    }

    return analysis