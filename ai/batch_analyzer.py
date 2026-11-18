from ai.resume_analyzer import analyze_resume


def analyze_multiple_resumes(job_description: str, candidates: list[dict]) -> list[dict]:
    """
    Analyze multiple candidates against one job description and rank them.
    """
    if not isinstance(job_description, str) or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    if not candidates:
        raise ValueError("At least one candidate is required.")

    results = []

    for candidate in candidates:
        filename = candidate.get("filename", "Unknown")
        resume_text = candidate.get("text", "")

        try:
            analysis = analyze_resume(
                resume_text,
                job_description
            )

            results.append({
                "filename": filename,
                "skill_match_score": analysis["skill_match_score"],
                "semantic_similarity_score": analysis["semantic_similarity_score"],
                "matched_skills": analysis["matched_skills"],
                "missing_skills": analysis["missing_skills"],
                "status": "Analyzed"
            })

        except Exception as error:
            # Kisi ek candidate ke error se baaki batch fail nahi hoga
            results.append({
                "filename": filename,
                "skill_match_score": None,
                "semantic_similarity_score": None,
                "matched_skills": [],
                "missing_skills": [],
                "status": f"Failed: {error}"
            })

    # Rank candidates with valid skill scores first
    results.sort(
        key=lambda item: (
            item["skill_match_score"] is not None,
            item["skill_match_score"] or 0,
            item["semantic_similarity_score"] or 0
        ),
        reverse=True
    )

    # Assign ranks only to successfully analyzed candidates
    rank = 1
    for result in results:
        if result["status"] == "Analyzed":
            result["rank"] = rank
            rank += 1
        else:
            result["rank"] = None

    return results