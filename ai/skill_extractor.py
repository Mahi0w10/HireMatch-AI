import re

SKILLS = [
    # Programming
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript",

    # Data Analysis
    "SQL", "MySQL", "PostgreSQL", "Excel", "Power BI",
    "Tableau", "Pandas", "NumPy", "Data Analysis",
    "Data Visualization", "Statistics", "Machine Learning",

    # Web Development
    "HTML", "CSS", "React", "Node.js", "FastAPI",
    "Flask", "REST API", "MongoDB", "SQLite",

    # Business Analysis
    "Business Analysis", "Requirements Gathering",
    "Requirement Analysis", "Business Intelligence",
    "Problem Solving", "Critical Thinking",
    "Communication", "Documentation", "Agile",
    "Project Management", "Stakeholder Management",

    # Other
    "Git", "GitHub", "Data Cleaning", "Data Modeling",
    "PowerPoint", "Presentation Skills"
]


def extract_skills(text):
    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_text, job_description):
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