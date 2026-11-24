# HireMatch AI — AI-Based Resume Screening & Job Matching System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.142-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.x-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Sentence--Transformers](https://img.shields.io/badge/Sentence--Transformers-all--MiniLM--L6--v2-orange.svg)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

An explainable, dual-metric AI platform designed to automate resume screening, evaluate candidate-job alignment, rank multi-applicant batches with tie-breaking logic, and provide actionable skill-gap diagnostics.

---

## 📌 Project Overview

In technical recruitment, HR teams face severe cognitive fatigue processing hundreds of resumes for single vacancies. Traditional ATS keyword search engines trigger high false-negative rates due to strict syntactic mismatch, while opaque black-box neural networks lack explainability.

**HireMatch AI** bridges this divide by delivering a transparent human-in-the-loop decision-support system:
1. **Candidate Self-Assessment:** Analyzes single resume PDFs against job descriptions, outputting explicit Skill Match (%) compliance, dense contextual Semantic Similarity (/100), and personalized skill-gap learning suggestions.
2. **Recruiter Batch Leaderboard:** Screens batches of up to 20 resumes simultaneously, generating an interactive ranked leaderboard with automated hierarchical tie-breaking.
3. **Persistent Shortlisting:** One-click recruiter shortlisting backed by an ACID-compliant SQLite transactional database.

---

## 🏗️ System Architecture

HireMatch AI follows a decoupled, **Three-Tier Function-Oriented Architecture**: