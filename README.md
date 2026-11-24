# HireMatch AI
### AI-Based Resume Screening & Job Matching System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.x-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Sentence Transformers](https://img.shields.io/badge/AI-SentenceTransformers-orange)](https://www.sbert.net/)

HireMatch AI is an AI-powered resume screening and job matching system designed to help candidates evaluate their resumes and assist recruiters in identifying suitable candidates efficiently.

The system combines lexical skill matching and semantic similarity analysis to provide transparent candidate evaluations, skill-gap insights, and automated resume ranking.

---

## 📌 Project Overview

Traditional resume screening often relies heavily on keyword matching, which can overlook relevant candidates when different terms describe similar skills.

HireMatch AI addresses this limitation through a dual-metric evaluation approach:

1. **Candidate Resume Analysis:** Evaluates a single resume against a job description and generates skill match scores, semantic similarity scores, matched skills, and missing skills.
2. **Recruiter Batch Screening:** Processes multiple resumes simultaneously and generates a ranked candidate leaderboard.
3. **Candidate Shortlisting:** Allows recruiters to shortlist suitable candidates and store their information in an SQLite database.
4. **Skill Gap Analysis:** Identifies missing skills and provides actionable suggestions for improvement.

---

## ✨ Key Features & Technical Highlights

- **100-Word Semantic Chunking:** Divides long resume text into logical chunks to reduce information loss caused by the model's input-length limit. Calculates similarity across chunks and averages the top three scores.
- **Canonical Skill Normalization:** Uses boundary-based regular expressions and alias mapping to identify and standardize skills. Examples: `PowerBI` → `Power BI`, `MS Excel` → `Excel`, and `JS` → `JavaScript`.
- **Dual-Metric Evaluation:** Combines lexical skill matching and semantic similarity to provide two separate evaluation scores.
- **Automated Candidate Ranking:** Ranks candidates using skill match percentage, with semantic similarity used as a tie-breaker.
- **Fault-Tolerant Batch Processing:** Handles failed or unreadable PDF files individually without interrupting the remaining batch evaluations.
- **Persistent Shortlisting:** Saves shortlisted candidate information in an SQLite database.

---

## 🏗️ System Architecture

HireMatch AI follows a three-tier architecture:

### 1. Frontend
- React.js
- JSX
- CSS3
- Vite
- Fetch API for backend communication

### 2. Backend
- Python 3.12
- FastAPI
- Uvicorn
- REST API endpoints

### 3. AI/NLP & Database
- PyMuPDF for PDF text extraction
- Regular Expressions and Alias Mapping for skill extraction
- Sentence Transformers (`all-MiniLM-L6-v2`) for semantic similarity
- Scikit-learn for cosine similarity calculations
- SQLite for persistent data storage

---

## 🧠 AI/NLP Processing Workflow

1. Resume PDF is uploaded by the candidate or recruiter.
2. PyMuPDF extracts text from the uploaded PDF.
3. Regex-based skill extraction identifies relevant skills.
4. Alias mapping normalizes different representations of the same skill.
5. The job description is analyzed to identify required skills.
6. Lexical skill matching calculates the skill match percentage.
7. Sentence Transformers generates semantic embeddings.
8. Chunk-based cosine similarity calculates semantic relevance.
9. The system generates evaluation results and candidate rankings.
10. Recruiters can shortlist candidates for future reference.

---

## 🔌 Backend API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root/status endpoint |
| GET | `/health` | Health check |
| POST | `/analyze-resume` | Analyze a single resume |
| POST | `/analyze-multiple-resumes` | Batch resume screening and ranking |
| POST | `/shortlist-candidate` | Save a shortlisted candidate |
| GET | `/shortlisted-candidates` | Retrieve shortlisted candidates |

Interactive API documentation is available through FastAPI Swagger UI after starting the backend:

`http://127.0.0.1:8000/docs`

---

## 🗄️ Database Design

HireMatch AI uses SQLite for persistent storage.

### 1. analysis_results
Stores resume evaluation information, including:
- Resume filename
- Job description
- Skill match score
- Semantic similarity score
- Matched skills
- Missing skills
- Candidate rank
- Creation timestamp

### 2. shortlists
Stores recruiter shortlisting information, including:
- Resume filename
- Job description
- Skill match score
- Shortlisting status
- Recruiter notes
- Shortlisting timestamp

Database file: `database/hirematch.db`

---

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, JSX, CSS3, Vite |
| Backend | Python 3.12, FastAPI, Uvicorn |
| PDF Processing | PyMuPDF |
| Skill Extraction | Regex, Alias Mapping |
| Semantic Matching | Sentence Transformers |
| AI Model | all-MiniLM-L6-v2 |
| Similarity Calculation | Scikit-learn |
| Database | SQLite |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.12
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Mahi0w10/HireMatch-AI.git
cd HireMatch-AI
```

### 2. Backend Setup

Create and activate a virtual environment:

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r backend/requirements.txt
```

Start the backend server:

```powershell
uvicorn backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

`http://localhost:5173`

---

## 🧪 Testing & Validation

The system has undergone functional and integration testing.

### Single Resume Analysis
- Tested using a real resume PDF containing approximately 4,407 characters.
- Generated a 44% skill match score.
- Generated a semantic similarity score of 40/100.
- Identified matched and missing skills.

### Batch Resume Screening
- Tested with five resumes simultaneously.
- Generated a ranked leaderboard.
- Successfully applied semantic similarity as a tie-breaker for candidates with identical skill match percentages.
- Verified that failed PDF processing does not interrupt the remaining batch.

### Database Integration
- Verified candidate shortlisting through the backend API.
- Confirmed that shortlisted candidate records were persisted in SQLite.

---

## 👥 Team Members & Contributions

| Team Member | Role | Contributions |
|---|---|---|
| Mahi Jha | Project Coordinator & AI/NLP Lead | Skill extraction, semantic matching, chunking, batch ranking, tie-breaking and integration |
| Ekta | Frontend Developer | React.js interface, JSX components and CSS styling |
| Tanishka | Backend & Database Engineer | SQLite integration, database schema and shortlist management |

---

## 🔮 Future Scope

- OCR support for scanned and image-based resumes.
- Advanced resume parsing and entity extraction.
- Recruiter authentication and role-based access.
- Advanced analytics and recruitment dashboards.
- Support for additional document formats.
- Further improvement of matching accuracy through evaluation on larger datasets.

---

## 🔒 Data Privacy

Candidate resume files and sensitive personal information are excluded from version control through `.gitignore` rules.

---

## 📄 License

This project was developed for academic purposes as part of the B.Tech CSE curriculum at Medi-Caps University, Indore.