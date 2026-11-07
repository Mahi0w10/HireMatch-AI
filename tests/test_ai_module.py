import sys
from pathlib import Path

# Main project folder ko Python path me add kar rahe hain
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai.skill_extractor import extract_skills, compare_skills
from ai.semantic_matcher import calculate_semantic_similarity
from ai.resume_analyzer import analyze_resume
from ai.batch_analyzer import analyze_multiple_resumes

print("=" * 60)
print("1. TESTING SKILL EXTRACTION & ALIASES")
print("=" * 60)
sample_text = "I have experience in PowerBI, MS Excel, JS, ML, and Python."
extracted = extract_skills(sample_text)
print("Input Text:", sample_text)
print("Skills Found:", extracted)

print("\n" + "=" * 60)
print("2. TESTING SEMANTIC SIMILARITY")
print("=" * 60)
resume_sample = "Experienced Python developer with strong SQL and Machine Learning knowledge."
jd_sample = "Looking for a Python Developer who knows Machine Learning and SQL databases."
similarity = calculate_semantic_similarity(resume_sample, jd_sample)
print(f"Semantic Match Score: {similarity}/100")

print("\n" + "=" * 60)
print("3. TESTING SINGLE RESUME ANALYZER")
print("=" * 60)
single_result = analyze_resume(resume_sample, jd_sample)
print(f"Skill Match Score: {single_result['skill_match_score']}%")
print(f"Matched Skills: {single_result['matched_skills']}")
print(f"Missing Skills: {single_result['missing_skills']}")
print(f"Explanation: {single_result['explanation']}")

print("\n" + "=" * 60)
print("4. TESTING BATCH ANALYZER (RANKING)")
print("=" * 60)
candidates = [
    {
        "filename": "Candidate_A.pdf",
        "text": "Only basic Python and HTML knowledge."
    },
    {
        "filename": "Candidate_B.pdf",
        "text": "Expert in Python, Machine Learning, SQL, and Excel."
    }
]
batch_results = analyze_multiple_resumes(jd_sample, candidates)
for candidate in batch_results:
    print(f"Rank {candidate['rank']}: {candidate['filename']} (Score: {candidate['skill_match_score']}%)")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED!")
print("=" * 60)
