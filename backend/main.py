
import pathlib
import traceback
from typing import Annotated

import pymupdf as fitz
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ai.resume_analyzer import analyze_resume
from ai.batch_analyzer import analyze_multiple_resumes
from database.db import (
    shortlist_candidate,
    get_shortlisted_candidates,
    save_analysis
)

app = fastapi.FastAPI(
    title="HireMatch AI",
    description="AI-Based Resume Screening and Job Matching System",
    version="1.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["openapi"] = "3.0.2"

    def fix_file_schema(schema):
        if isinstance(schema, dict):
            if schema.get("contentMediaType") == "application/octet-stream":
                schema.pop("contentMediaType", None)
                schema["format"] = "binary"

            for value in schema.values():
                if isinstance(value, (dict, list)):
                    fix_file_schema(value)

        elif isinstance(schema, list):
            for item in schema:
                fix_file_schema(item)

    fix_file_schema(openapi_schema.get("components", {}).get("schemas", {}))

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

RESUME_DIR = pathlib.Path("resumes")
RESUME_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND_DIR = pathlib.Path("frontend")
FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")


class ShortlistRequest(BaseModel):
    filename: str
    job_description: str
    skill_match_score: float | None = None
    notes: str = ""


@app.get("/")
def home():
    return {
        "message": "Welcome to HireMatch AI!",
        "status": "running",
        "web_ui": "Open /ui in your browser to access the Web Dashboard."
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


async def read_resume_pdf(file: fastapi.UploadFile) -> bytes:
    if not file.filename or pathlib.Path(file.filename).suffix.lower() != ".pdf":
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"File '{file.filename}' is not a PDF. Please upload PDF files only."
        )

    content = await file.read()

    if not content.startswith(b"%PDF-"):
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"File '{file.filename}' is not a valid PDF file."
        )

    return content


def extract_text_from_pdf(content: bytes) -> str:
    try:
        with fitz.open(stream=content, filetype="pdf") as pdf:
            extracted_text = "\n".join(
                page.get_text() for page in pdf
            ).strip()

    except Exception:
        raise fastapi.HTTPException(
            status_code=400,
            detail="Could not read the PDF file."
        )

    if not extracted_text:
        raise fastapi.HTTPException(
            status_code=422,
            detail="No readable text found in this PDF. Scanned PDFs may need OCR."
        )

    return extracted_text


@app.post("/upload-resume")
async def upload_resume(
    file: Annotated[
        fastapi.UploadFile,
        fastapi.File(description="Choose a PDF resume.")
    ]
):
    content = await read_resume_pdf(file)
    safe_filename = pathlib.Path(file.filename).name
    file_path = RESUME_DIR / safe_filename

    try:
        file_path.write_bytes(content)
    except OSError:
        raise fastapi.HTTPException(
            status_code=500,
            detail="Could not save the uploaded resume."
        )

    return {
        "message": "Resume uploaded successfully!",
        "filename": safe_filename,
        "size_bytes": len(content)
    }


@app.post("/extract-resume-text")
async def extract_resume_text(
    file: Annotated[
        fastapi.UploadFile,
        fastapi.File(description="Choose a PDF resume.")
    ]
):
    content = await read_resume_pdf(file)
    extracted_text = extract_text_from_pdf(content)

    return {
        "message": "Resume text extracted successfully!",
        "filename": pathlib.Path(file.filename).name,
        "text": extracted_text,
        "characters": len(extracted_text)
    }


@app.post("/analyze-resume")
async def analyze_resume_api(
    file: Annotated[
        fastapi.UploadFile,
        fastapi.File(description="Choose a PDF resume.")
    ],
    job_description: Annotated[
        str,
        fastapi.Form(description="Paste the job description.")
    ]
):
    if not job_description.strip():
        raise fastapi.HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    content = await read_resume_pdf(file)
    resume_text = extract_text_from_pdf(content)
    filename = pathlib.Path(file.filename).name

    try:
        result = analyze_resume(resume_text, job_description)

        save_analysis(
            filename=filename,
            job_description=job_description,
            skill_match_score=result["skill_match_score"],
            semantic_similarity_score=result["semantic_similarity_score"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"]
        )

    except ValueError as error:
        raise fastapi.HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        print("\n===== RESUME ANALYSIS ERROR =====")
        traceback.print_exc()

        raise fastapi.HTTPException(
            status_code=500,
            detail=str(error)
        )

    return {
        "message": "Resume analysis completed successfully!",
        "filename": filename,
        "analysis": result
    }


@app.post("/analyze-multiple-resumes")
async def analyze_multiple_resumes_api(
    files: Annotated[
        list[fastapi.UploadFile],
        fastapi.File(description="Choose one or more PDF resumes.")
    ],
    job_description: Annotated[
        str,
        fastapi.Form(description="Paste the job description.")
    ]
):
    if not job_description.strip():
        raise fastapi.HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    if not files:
        raise fastapi.HTTPException(
            status_code=400,
            detail="Upload at least one resume."
        )

    if len(files) > 20:
        raise fastapi.HTTPException(
            status_code=400,
            detail="You can upload a maximum of 20 resumes at a time."
        )

    candidates = []
    invalid_files = []

    for file in files:
        filename = pathlib.Path(file.filename).name if file.filename else "Unknown"

        try:
            content = await read_resume_pdf(file)
            resume_text = extract_text_from_pdf(content)

            candidates.append({
                "filename": filename,
                "text": resume_text
            })

        except fastapi.HTTPException as error:
            invalid_files.append({
                "filename": filename,
                "status": "Failed",
                "error": error.detail
            })

        finally:
            await file.close()

    if not candidates:
        raise fastapi.HTTPException(
            status_code=422,
            detail={
                "message": "No valid, readable PDF resumes were uploaded.",
                "invalid_files": invalid_files
            }
        )

    try:
        results = analyze_multiple_resumes(job_description, candidates)

        for cand in results:
            if cand["status"] == "Analyzed":
                save_analysis(
                    filename=cand["filename"],
                    job_description=job_description,
                    skill_match_score=cand["skill_match_score"],
                    semantic_similarity_score=cand["semantic_similarity_score"],
                    matched_skills=cand["matched_skills"],
                    missing_skills=cand["missing_skills"],
                    rank=cand.get("rank")
                )

    except ValueError as error:
        raise fastapi.HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        print("\n===== MULTIPLE RESUME ANALYSIS ERROR =====")
        traceback.print_exc()

        raise fastapi.HTTPException(
            status_code=500,
            detail=str(error)
        )

    return {
        "message": "Multiple resume analysis completed.",
        "total_uploaded": len(files),
        "total_analyzed": len(candidates),
        "total_failed": len(invalid_files),
        "results": results,
        "invalid_files": invalid_files
    }


@app.post("/shortlist-candidate")
def shortlist_candidate_api(request: ShortlistRequest):
    record_id = shortlist_candidate(
        filename=request.filename,
        job_description=request.job_description,
        skill_match_score=request.skill_match_score,
        notes=request.notes
    )

    return {
        "message": f"Candidate '{request.filename}' shortlisted successfully!",
        "id": record_id,
        "status": "Shortlisted"
    }


@app.get("/shortlisted-candidates")
def get_shortlisted_candidates_api():
    candidates = get_shortlisted_candidates()

    return {
        "total_shortlisted": len(candidates),
        "candidates": candidates
    }
