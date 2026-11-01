from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pathlib import Path
import fitz

from ai.resume_analyzer import analyze_resume


app = FastAPI(
    title="HireMatch AI",
    description="AI-Based Resume Screening and Job Matching System",
    version="1.0.0"
)

RESUME_DIR = Path("resumes")
RESUME_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to HireMatch AI!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    content = await file.read()

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF."
        )

    safe_filename = Path(file.filename).name
    file_path = RESUME_DIR / safe_filename

    try:
        file_path.write_bytes(content)
    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Could not save the uploaded resume."
        )

    return {
        "message": "Resume uploaded successfully!",
        "filename": safe_filename,
        "size_bytes": len(content)
    }


@app.post("/extract-resume-text")
async def extract_resume_text(file: UploadFile = File(...)):

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    content = await file.read()

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF."
        )

    try:
        with fitz.open(stream=content, filetype="pdf") as pdf:
            extracted_text = "\n".join(
                page.get_text() for page in pdf
            ).strip()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the PDF file."
        )

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text found in this PDF."
        )

    return {
        "message": "Resume text extracted successfully!",
        "filename": Path(file.filename).name,
        "text": extracted_text,
        "characters": len(extracted_text)
    }


@app.post("/analyze-resume")
async def analyze_resume_api(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    content = await file.read()

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF."
        )

    try:
        with fitz.open(stream=content, filetype="pdf") as pdf:
            resume_text = "\n".join(
                page.get_text() for page in pdf
            ).strip()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the PDF file."
        )

    if not resume_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text found in this PDF."
        )

    try:
        result = analyze_resume(
            resume_text,
            job_description
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed. Please try again."
        )

    return {
        "message": "Resume analysis completed successfully!",
        "filename": Path(file.filename).name,
        "analysis": result
    }