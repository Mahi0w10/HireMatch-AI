# HireMatch AI — Frontend

The frontend of HireMatch AI is developed using React.js, JSX, CSS3, and Vite. It provides an interactive interface for candidates and recruiters to access resume analysis and screening features.

## ✨ Features

- **Single Resume Analysis:** Upload a resume and job description to view evaluation results.
- **Batch Resume Screening:** Upload multiple resumes and view the ranked candidate leaderboard.
- **Shortlisted Candidates:** View candidates saved by recruiters.
- **Results Display:** View skill match scores, semantic similarity scores, matched skills, and missing skills.
- **Backend Integration:** Communicates with the FastAPI backend using the Fetch API.

## 🛠️ Technology Stack

- React.js
- JSX
- CSS3
- Vite
- JavaScript
- Fetch API

## 📁 Project Structure

The frontend is maintained in the `frontend/` directory of the main repository.

```text
frontend/
├── public/
├── src/
│   ├── App.jsx
│   ├── Results.jsx
│   └── ...
├── index.html
├── package.json
└── vite.config.js
```

*Note: Update this structure if the actual frontend directory contains additional or differently named files.*

## 🚀 Getting Started

### Prerequisites

- Node.js
- npm

### Installation

```bash
cd frontend
npm install
```

### Run Development Server

```bash
npm run dev
```

The Vite development server generally runs at:

`http://localhost:5173`

## 🔗 Backend Connection

The frontend communicates with the FastAPI backend through HTTP requests using the Fetch API.

The backend should be running at:

`http://127.0.0.1:8000`

The backend provides endpoints for single resume analysis, batch screening, and candidate shortlisting.

## 👥 Contribution

Developed by Ekta as part of the HireMatch AI project team.