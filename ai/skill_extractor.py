import re

# Standard aliases mapping for skills (Synonyms normalization)
SKILL_ALIASES = {
    "PowerBI": "Power BI",
    "MS Excel": "Excel",
    "Microsoft Excel": "Excel",
    "Postgre SQL": "PostgreSQL",
    "JS": "JavaScript",
    "ML": "Machine Learning",
    "Data Analytics": "Data Analysis",
    "ReactJS": "React",
    "React.js": "React",
    "NodeJS": "Node.js",
}

# Recognized skills dictionary
SKILLS = [
    # Programming
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript",

    # Data Analysis
    "SQL", "MySQL", "PostgreSQL", "Excel", "Advanced Excel",
    "Power BI", "Tableau", "Pandas", "NumPy",
    "Data Analysis", "Data Visualization",
    "Statistics", "Machine Learning", "Data Cleaning",
    "Data Modeling", "Dashboard Development", "Reporting",

    # Business Analysis
    "Business Analysis",
    "Requirements Gathering", "Requirement Analysis",
    "Requirements Analysis", "Business Intelligence",
    "Stakeholder Management", "Process Mapping",
    "Gap Analysis", "Documentation", "Agile",
    "Project Management", "Problem Solving",
    "Critical Thinking", "Communication",

    # Web Development
    "HTML", "CSS", "React", "Node.js", "FastAPI",
    "Flask", "REST API", "MongoDB", "SQLite",

    # Tools
    "Git", "GitHub", "PowerPoint", "Presentation Skills"
]


def extract_skills(text: str) -> list[str]:
    """
    Extracts recognized skills from text, handling known aliases and word boundaries.
    """
    if not isinstance(text, str) or not text.strip():
        return []

    normalized_text = text

    # Step 1: Replace known aliases with canonical names
    for alias, canonical in SKILL_ALIASES.items():
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        normalized_text = re.sub(
            pattern,
            canonical,
            normalized_text,
            flags=re.IGNORECASE
        )

    found_skills = []

    # Step 2: Extract skills using regex boundary checks
    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, normalized_text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_text: str, job_description: str) -> dict:
    """
    Compares extracted skills between a resume and a job description.
    """
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    match_score = (
        round(len(matched_skills) / len(job_skills) * 100)
        if job_skills else 0
    )

    return {
        "match_score": match_score,
        "resume_skills": resume_skills,
        "required_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
