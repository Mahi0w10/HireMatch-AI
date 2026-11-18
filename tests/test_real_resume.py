import sys
from pathlib import Path
import pymupdf as fitz

# Path setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai.resume_analyzer import analyze_resume

# 1. Resumes folder se PDF dhoondhte hain
resume_dir = Path("resumes")
pdf_files = list(resume_dir.glob("*.pdf"))

if not pdf_files:
    print("ERROR: resumes/ folder me koi PDF nahi mila!")
    sys.exit(1)

target_pdf = pdf_files[0]
print("=" * 60)
print(f"TESTING REAL RESUME: {target_pdf.name}")
print("=" * 60)

# 2. Text extract karte hain
with fitz.open(target_pdf) as doc:
    extracted_text = "\n".join(page.get_text() for page in doc).strip()

print(f"Extracted Characters: {len(extracted_text)}")

# 3. Sample Job Description
sample_jd = """
We are looking for a Data Analyst / Python Developer.
Required Skills: Python, SQL, Power BI, Excel, Machine Learning, Data Analysis.
Responsibilities include dashboard development, data modeling, and reporting.
"""

print("\n" + "=" * 60)
print("ANALYZING RESUME AGAINST JOB DESCRIPTION")
print("=" * 60)

analysis = analyze_resume(extracted_text, sample_jd)

print(f"Skill Match Score: {analysis['skill_match_score']}%")
print(f"Semantic Similarity: {analysis['semantic_similarity_score']}/100")
print(f"\nMatched Skills: {analysis['matched_skills']}")
print(f"Missing Skills: {analysis['missing_skills']}")
print(f"\nExplanation:\n{analysis['explanation']}")
print("=" * 60)
