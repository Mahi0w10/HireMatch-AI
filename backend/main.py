from fastapi import FastAPI

app = FastAPI(
    title="HireMatch AI",
    description="AI-Based Resume Screening and Job Matching System",
    version="1.0.0"
)


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