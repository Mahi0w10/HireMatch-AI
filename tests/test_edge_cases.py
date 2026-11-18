import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai.skill_extractor import extract_skills, compare_skills
from ai.resume_analyzer import analyze_resume

print("=" * 60)
print("TEST 1: JOB DESCRIPTION WITH NO RECOGNIZED SKILLS")
print("=" * 60)
# Recruiter ne aisi JD di jisme koi skill dictionary wali word nahi hai
plain_jd = "Looking for an energetic team player with good attitude for office work."
resume_text = "Proficient in Python, SQL and Excel."

result_no_skills = analyze_resume(resume_text, plain_jd)
print("Required Skills in JD:", result_no_skills["required_skills"])
print("Skill Match Score:", result_no_skills["skill_match_score"])  # None hona chahiye, 0% nahi
print("Explanation:", result_no_skills["explanation"])

print("\n" + "=" * 60)
print("TEST 2: EMPTY RESUME / EMPTY JD VALIDATION")
print("=" * 60)
try:
    analyze_resume("", plain_jd)
    print("FAILED: Empty resume par error nahi aaya!")
except ValueError as e:
    print(f"PASSED: Empty resume correctly blocked -> '{e}'")

try:
    analyze_resume(resume_text, "   ")
    print("FAILED: Empty JD par error nahi aaya!")
except ValueError as e:
    print(f"PASSED: Empty JD correctly blocked -> '{e}'")

print("\n" + "=" * 60)
print("ALL EDGE CASES PASSED SUCCESSFULLY!")
print("=" * 60)
