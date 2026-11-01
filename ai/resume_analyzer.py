from ai.skill_extractor import compare_skills


def analyze_resume(resume_text, job_description):
    # Compare resume skills with job requirements
    result = compare_skills(resume_text, job_description)

    # Prepare analysis output
    analysis = {
        "match_score": result["match_score"],
        "resume_skills": result["resume_skills"],
        "required_skills": result["required_skills"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "explanation": (
            f"Matched {len(result['matched_skills'])} out of "
            f"{len(result['required_skills'])} identified required skills."
        ),
        "suggestions": [
            f"Consider developing your {skill} skills."
            for skill in result["missing_skills"]
        ]
    }

    return analysis