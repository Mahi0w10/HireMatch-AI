import React, { useEffect, useState } from "react";
import { BrowserRouter, useLocation, useNavigate } from "react-router-dom";

import "./App.css";
import Results from "./Results";

const API_URL = "http://127.0.0.1:8000";

// FORMAT JOB DESCRIPTION
function renderFormattedDescription(description) {
  const lines = (description || "").split(/\r?\n/);
  const elements = [];
  let bulletItems = [];

  const formatBold = (text) => {
    return text.split(/(\*\*.*?\*\*)/g).map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={index}>
            {part.slice(2, -2)}
          </strong>
        );
      }

      return part;
    });
  };

  const flushBullets = () => {
    if (bulletItems.length > 0) {
      elements.push(
        <ul
          key={`list-${elements.length}`}
          style={{
            paddingLeft: "22px",
            margin: "8px 0 14px",
          }}
        >
          {bulletItems.map((item, index) => (
            <li
              key={index}
              style={{ marginBottom: "7px" }}
            >
              {formatBold(item)}
            </li>
          ))}
        </ul>
      );

      bulletItems = [];
    }
  };

  lines.forEach((line, index) => {
    const trimmedLine = line.trim();

    if (!trimmedLine) {
      flushBullets();
      return;
    }

    if (trimmedLine.startsWith("- ")) {
      bulletItems.push(trimmedLine.slice(2));
      return;
    }

    flushBullets();

    const heading = trimmedLine.match(/^\*\*(.*?)\*\*:?$/);

    if (heading) {
      elements.push(
        <h4
          key={index}
          style={{
            margin: "16px 0 7px",
            color: "#285c38",
          }}
        >
          {heading[1]}
        </h4>
      );
    } else {
      elements.push(
        <p
          key={index}
          style={{
            margin: "7px 0",
            lineHeight: 1.7,
          }}
        >
          {formatBold(trimmedLine)}
        </p>
      );
    }
  });

  flushBullets();

  return elements;
}

// PAGE ROUTES
const PAGE_PATHS = {
  home: "/",
  seeker: "/seeker",
  results: "/results",
  recruiter: "/recruiter",
  "recruiter-results": "/recruiter-results",
};

function getPageFromPath(pathname) {
  const match = Object.entries(PAGE_PATHS).find(
    ([, path]) => path === pathname
  );

  return match ? match[0] : "home";
}

// SAFE SESSION STORAGE READER
function readSessionValue(key, fallback) {
  try {
    const value = sessionStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
}

// MAIN APP CONTENT
function AppContent() {
  const navigate = useNavigate();
  const location = useLocation();

  const [page, setPage] = useState(() =>
    getPageFromPath(location.pathname)
  );

  const navigateTo = (nextPage) => {
    navigate(PAGE_PATHS[nextPage] || "/");
  };

  // UPDATE PAGE WHEN URL CHANGES
  useEffect(() => {
    setPage(getPageFromPath(location.pathname));
  }, [location.pathname]);

  // JOB SEEKER STATES
  const [selectedResume, setSelectedResume] = useState(null);
  const [resumeError, setResumeError] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  // RECRUITER STATES
  const [candidateResumes, setCandidateResumes] = useState([]);
  const [recruiterResumeError, setRecruiterResumeError] = useState("");

  const [recruiterJobTitle, setRecruiterJobTitle] = useState(
    () => sessionStorage.getItem("hirematch_recruiter_job_title") || ""
  );

  const [recruiterJobDescription, setRecruiterJobDescription] = useState(
    () => sessionStorage.getItem("hirematch_recruiter_job_description") || ""
  );

  const [recruiterResults, setRecruiterResults] = useState(
    () => readSessionValue("hirematch_recruiter_results", null)
  );

  const [recruiterLoading, setRecruiterLoading] = useState(false);
  const [recruiterApiError, setRecruiterApiError] = useState("");

  // SHORTLIST STATES
  const [shortlistedCandidates, setShortlistedCandidates] = useState([]);
  const [shortlistMessages, setShortlistMessages] = useState({});
  const [shortlistLoading, setShortlistLoading] = useState({});

  // ERROR MESSAGE HANDLER
  const getErrorMessage = (data) => {
    if (typeof data?.detail === "string") {
      return data.detail;
    }

    if (Array.isArray(data?.detail)) {
      return data.detail
        .map((item) => item.msg || "Invalid input")
        .join(", ");
    }

    return data?.message || "Something went wrong. Please try again.";
  };

  // JOB SEEKER FILE VALIDATION
  const handleResumeChange = (event) => {
    const file = event.target.files[0];

    setResumeError("");
    setApiError("");
    setSelectedResume(null);
    setAnalysis(null);

    if (!file) return;

    const extension = file.name
      .slice(file.name.lastIndexOf("."))
      .toLowerCase();

    if (extension !== ".pdf") {
      setResumeError("Please upload a PDF resume.");
      event.target.value = "";
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setResumeError("Resume size must be 10 MB or less.");
      event.target.value = "";
      return;
    }

    setSelectedResume(file);
  };

  // RECRUITER MULTIPLE FILE VALIDATION
  const handleCandidateResumesChange = (event) => {
    const files = Array.from(event.target.files);

    setRecruiterResumeError("");
    setRecruiterApiError("");
    setCandidateResumes([]);
    setRecruiterResults(null);

    if (files.length === 0) return;

    const invalidFile = files.find((file) => {
      const extension = file.name
        .slice(file.name.lastIndexOf("."))
        .toLowerCase();

      return extension !== ".pdf";
    });

    if (invalidFile) {
      setRecruiterResumeError(
        "Only PDF resume files are allowed."
      );

      event.target.value = "";
      return;
    }

    const oversizedFile = files.find(
      (file) => file.size > 10 * 1024 * 1024
    );

    if (oversizedFile) {
      setRecruiterResumeError(
        "Each resume must be 10 MB or less."
      );

      event.target.value = "";
      return;
    }

    setCandidateResumes(files);
  };

  // JOB SEEKER RESUME ANALYSIS
  const handleAnalyzeResume = async (event) => {
    event.preventDefault();

    setResumeError("");
    setApiError("");

    if (!selectedResume) {
      setResumeError("Please upload your resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setApiError("Please enter a job description.");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("file", selectedResume);
      formData.append("job_description", jobDescription.trim());

      const response = await fetch(
        `${API_URL}/analyze-resume`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(getErrorMessage(data));
      }

      if (!data.analysis) {
        throw new Error("Analysis data was not returned.");
      }

      setAnalysis(data.analysis);
      navigateTo("results");
    } catch (error) {
      setApiError(
        error.message || "Unable to analyze your resume."
      );
    } finally {
      setLoading(false);
    }
  };

  // FETCH SHORTLISTED CANDIDATES
  const fetchShortlistedCandidates = async () => {
    try {
      const response = await fetch(
        `${API_URL}/shortlisted-candidates`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(getErrorMessage(data));
      }

      setShortlistedCandidates(data.candidates || []);
    } catch (error) {
      console.error(
        "Unable to fetch shortlisted candidates:",
        error
      );
    }
  };

  // REFRESH SHORTLIST WHEN RECRUITER RESULTS PAGE OPENS
  useEffect(() => {
    if (page === "recruiter-results") {
      fetchShortlistedCandidates();
    }
  }, [page]);

  // RECRUITER MULTIPLE RESUME ANALYSIS
  const handleAnalyzeCandidates = async (event) => {
    event.preventDefault();

    setRecruiterApiError("");
    setRecruiterResumeError("");

    if (!recruiterJobTitle.trim()) {
      setRecruiterApiError("Please enter a job title.");
      return;
    }

    if (!recruiterJobDescription.trim()) {
      setRecruiterApiError("Please enter a job description.");
      return;
    }

    if (candidateResumes.length === 0) {
      setRecruiterResumeError(
        "Please upload at least one resume."
      );
      return;
    }

    try {
      setRecruiterLoading(true);
      setShortlistMessages({});

      const completeJobDescription =
        `Job Title: ${recruiterJobTitle.trim()}\n\n` +
        recruiterJobDescription.trim();

      const formData = new FormData();

      formData.append(
        "job_description",
        completeJobDescription
      );

      candidateResumes.forEach((file) => {
        formData.append("files", file);
      });

      const response = await fetch(
        `${API_URL}/analyze-multiple-resumes`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(getErrorMessage(data));
      }

      setRecruiterResults(data);

      // SAVE RECRUITER RESULTS IN SESSION STORAGE
      sessionStorage.setItem(
        "hirematch_recruiter_results",
        JSON.stringify(data)
      );

      sessionStorage.setItem(
        "hirematch_recruiter_job_title",
        recruiterJobTitle
      );

      sessionStorage.setItem(
        "hirematch_recruiter_job_description",
        recruiterJobDescription
      );

      await fetchShortlistedCandidates();

      navigateTo("recruiter-results");
    } catch (error) {
      setRecruiterApiError(
        error.message || "Unable to analyze candidate resumes."
      );
    } finally {
      setRecruiterLoading(false);
    }
  };

  // SHORTLIST A CANDIDATE
  const handleShortlistCandidate = async (candidate) => {
    const filename = candidate.filename;

    const completeJobDescription =
      `Job Title: ${recruiterJobTitle.trim()}\n\n` +
      recruiterJobDescription.trim();

    try {
      setShortlistLoading((previous) => ({
        ...previous,
        [filename]: true,
      }));

      setShortlistMessages((previous) => ({
        ...previous,
        [filename]: "",
      }));

      const response = await fetch(
        `${API_URL}/shortlist-candidate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            filename: filename,
            job_description: completeJobDescription,
            skill_match_score: candidate.skill_match_score,
            notes: "Shortlisted from HireMatch AI recruiter dashboard.",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(getErrorMessage(data));
      }

      setShortlistMessages((previous) => ({
        ...previous,
        [filename]: data.message || "Candidate shortlisted successfully!",
      }));

      await fetchShortlistedCandidates();
    } catch (error) {
      setShortlistMessages((previous) => ({
        ...previous,
        [filename]:
          error.message || "Unable to shortlist candidate.",
      }));
    } finally {
      setShortlistLoading((previous) => ({
        ...previous,
        [filename]: false,
      }));
    }
  };

  // INLINE DASHBOARD STYLES
  const dashboardCardStyle = {
    background: "#ffffff",
    border: "1px solid #e9e7ed",
    borderRadius: "18px",
    padding: "25px",
    marginBottom: "20px",
    boxShadow: "0 5px 18px rgba(35, 30, 55, 0.04)",
  };

  const skillStyle = {
    display: "inline-flex",
    alignItems: "center",
    background: "#e5f2e6",
    color: "#285c38",
    padding: "8px 13px",
    borderRadius: "20px",
    fontSize: "12px",
    fontWeight: "600",
    margin: 0,
    lineHeight: 1.5,
  };

  const missingSkillStyle = {
    ...skillStyle,
    background: "#fff0e9",
    color: "#a54b2b",
  };

  // RECRUITER RESULTS
  const candidateResults = recruiterResults?.results || [];

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">
        <button
          className="brand"
          onClick={() => navigateTo("home")}
        >
          HireMatch<span>.AI</span>
        </button>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
        </div>

        <button
          className="nav-button"
          onClick={() => navigateTo("recruiter")}
        >
          Recruiter Portal ↗
        </button>
      </nav>

      {/* HOME PAGE */}
      {page === "home" && (
        <>
          <main className="hero">

            <div className="hero-badge">
              <span className="status-dot"></span>
              YOUR NEXT CAREER MOVE STARTS HERE
            </div>

            <h1>
              The right talent.
              <br />
              <span>The right opportunity.</span>
            </h1>

            <p className="hero-description">
              Meet your smarter hiring companion. Match skills,
              discover opportunities, and make better career
              decisions with AI.
            </p>

            <div className="role-grid">

              <button
                className="role-card seeker-card"
                onClick={() => navigateTo("seeker")}
              >
                <span className="role-icon">💼</span>
                <span className="role-label">FOR JOB SEEKERS</span>

                <strong>Find your perfect match</strong>

                <span className="role-description">
                  Upload your resume and discover how well
                  you fit a job.
                </span>

                <span className="role-link">
                  Check my match <span>→</span>
                </span>
              </button>

              <button
                className="role-card recruiter-card"
                onClick={() => navigateTo("recruiter")}
              >
                <span className="role-icon">🤝</span>
                <span className="role-label">FOR RECRUITERS</span>

                <strong>Discover exceptional talent</strong>

                <span className="role-description">
                  Create job listings and rank candidates
                  by their skills.
                </span>

                <span className="role-link">
                  Find talent <span>→</span>
                </span>
              </button>

            </div>

            <div className="trust-line">
              <span>✳</span>
              Smarter matching. More meaningful careers.
            </div>

          </main>

          {/* FEATURES */}
          <section className="features-section" id="features">

            <div className="section-kicker">
              BUILT FOR BOTH SIDES
            </div>

            <h2>One platform. Better matches.</h2>

            <p className="section-description">
              Everything you need to make the next
              professional connection.
            </p>

            <div className="features-grid">

              <article className="feature-card">
                <div className="feature-icon">📄</div>
                <h3>Resume insights</h3>
                <p>
                  Understand how your experience aligns
                  with job requirements.
                </p>
              </article>

              <article className="feature-card">
                <div className="feature-icon">🎯</div>
                <h3>Skill matching</h3>
                <p>
                  Focus on relevant skills and identify
                  areas to improve.
                </p>
              </article>

              <article className="feature-card">
                <div className="feature-icon">📊</div>
                <h3>Candidate ranking</h3>
                <p>
                  Help recruiters organise candidates
                  against a job's needs.
                </p>
              </article>

            </div>
          </section>

          {/* HOW IT WORKS */}
          <section className="how-section" id="how-it-works">

            <div className="section-kicker">
              SIMPLE BY DESIGN
            </div>

            <h2>Your next step, made simpler.</h2>

            <div className="steps-grid">

              <div className="step-card">
                <span>01</span>
                <h3>Share your details</h3>
                <p>
                  Upload a resume or describe the role
                  you need to fill.
                </p>
              </div>

              <div className="step-card">
                <span>02</span>
                <h3>Compare skills</h3>
                <p>
                  Review the information against
                  the job requirements.
                </p>
              </div>

              <div className="step-card">
                <span>03</span>
                <h3>Move forward</h3>
                <p>
                  Use the insights to guide your next
                  hiring or career step.
                </p>
              </div>

            </div>
          </section>
        </>
      )}

      {/* JOB SEEKER PAGE */}
      {page === "seeker" && (
        <main className="workspace">

          <button
            className="back-button"
            onClick={() => navigateTo("home")}
          >
            ← Back to home
          </button>

          <div className="section-kicker">
            JOB SEEKER WORKSPACE
          </div>

          <h1>
            Find your <span>best match.</span>
          </h1>

          <p className="workspace-description">
            Add your resume and the job description
            you want to explore.
          </p>

          <form
            className="workspace-form"
            onSubmit={handleAnalyzeResume}
          >

            <label htmlFor="resume">
              Upload your resume (PDF only)
            </label>

            <input
              id="resume"
              type="file"
              accept=".pdf"
              required
              onChange={handleResumeChange}
            />

            {resumeError && (
              <p className="form-error">
                {resumeError}
              </p>
            )}

            {selectedResume && (
              <p className="form-success">
                Selected resume: {selectedResume.name}
              </p>
            )}

            <label htmlFor="job-description">
              Job description
            </label>

            <textarea
              id="job-description"
              rows="7"
              placeholder="Paste the job description here, including required skills, experience, and responsibilities..."
              minLength={30}
              maxLength={5000}
              required
              value={jobDescription}
              onChange={(event) =>
                setJobDescription(event.target.value)
              }
            />

            <p className="form-note">
              Include the job responsibilities, required
              skills, and experience. (30–5000 characters)
            </p>

            {apiError && (
              <p className="form-error">
                {apiError}
              </p>
            )}

            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Analyzing Resume..."
                : "Analyze My Resume →"}
            </button>

            {loading && (
              <p className="form-note">
                Please wait while HireMatch AI analyzes your resume.
              </p>
            )}

          </form>
        </main>
      )}

      {/* JOB SEEKER RESULTS */}
      {page === "results" && (
        <Results
          onBack={() => navigateTo("seeker")}
          resumeName={selectedResume?.name}
          jobDescription={jobDescription}
          analysis={analysis}
        />
      )}

      {/* RECRUITER FORM */}
      {page === "recruiter" && (
        <main className="workspace">

          <button
            className="back-button"
            onClick={() => navigateTo("home")}
          >
            ← Back to home
          </button>

          <div className="section-kicker">
            RECRUITER WORKSPACE
          </div>

          <h1>
            Build your <span>dream team.</span>
          </h1>

          <p className="workspace-description">
            Create a job listing and add candidate
            resumes for review.
          </p>

          <form
            className="workspace-form"
            onSubmit={handleAnalyzeCandidates}
          >

            <label htmlFor="job-title">
              Job title
            </label>

            <input
              id="job-title"
              type="text"
              placeholder="e.g. Data Analyst Intern"
              minLength={2}
              maxLength={80}
              required
              value={recruiterJobTitle}
              onChange={(event) =>
                setRecruiterJobTitle(event.target.value)
              }
            />

            <label htmlFor="job-details">
              Job description and required skills
            </label>

            <textarea
              id="job-details"
              rows="8"
              placeholder="Describe the role, responsibilities, qualifications, and required skills..."
              minLength={30}
              maxLength={5000}
              required
              value={recruiterJobDescription}
              onChange={(event) =>
                setRecruiterJobDescription(event.target.value)
              }
            />

            <label htmlFor="candidate-resumes">
              Upload candidate resumes (PDF only)
            </label>

            <input
              id="candidate-resumes"
              type="file"
              accept=".pdf"
              multiple
              required
              onChange={handleCandidateResumesChange}
            />

            {recruiterResumeError && (
              <p className="form-error">
                {recruiterResumeError}
              </p>
            )}

            {candidateResumes.length > 0 && (
              <div className="candidate-preview">
                <h3>
                  Selected Resumes ({candidateResumes.length})
                </h3>

                {candidateResumes.map((file, index) => (
                  <p key={`${file.name}-${index}`}>
                    📄 {file.name}
                  </p>
                ))}
              </div>
            )}

            {recruiterApiError && (
              <p className="form-error">
                {recruiterApiError}
              </p>
            )}

            <button
              className="primary-button"
              type="submit"
              disabled={recruiterLoading}
            >
              {recruiterLoading
                ? "Analyzing Candidates..."
                : "Analyze Candidates →"}
            </button>

            {recruiterLoading && (
              <p className="form-note">
                Please wait. Your resumes are being processed.
              </p>
            )}

          </form>
        </main>
      )}

      {/* RECRUITER RESULTS DASHBOARD */}
      {page === "recruiter-results" && (
        <main
          style={{
            minHeight: "80vh",
            background: "#f8f7fc",
            padding: "30px 7% 70px",
          }}
        >

          <div
            style={{
              maxWidth: "1150px",
              margin: "0 auto",
            }}
          >

            <button
              className="back-button"
              onClick={() => navigateTo("recruiter")}
            >
              ← Back to Recruiter Form
            </button>

            <div
              style={{
                textAlign: "center",
                margin: "20px 0 35px",
              }}
            >

              <div className="section-kicker">
                RECRUITER WORKSPACE
              </div>

              <h1
                style={{
                  color: "#211d35",
                  fontSize: "clamp(30px, 4vw, 42px)",
                  margin: "8px 0",
                }}
              >
                Candidate analysis.
              </h1>

              <p
                style={{
                  color: "#686477",
                  lineHeight: 1.7,
                }}
              >
                Review candidate matches and shortlist suitable profiles.
              </p>

            </div>

            {/* JOB DETAILS */}
            <section style={dashboardCardStyle}>

              <h2
                style={{
                  color: "#285c38",
                  marginTop: 0,
                }}
              >
                💼 {recruiterJobTitle}
              </h2>

              <div
                style={{
                  color: "#686477",
                  lineHeight: 1.7,
                }}
              >
                {renderFormattedDescription(
                  recruiterJobDescription
                )}
              </div>

            </section>

            {/* SUMMARY CARDS */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit, minmax(180px, 1fr))",
                gap: "16px",
                marginBottom: "35px",
              }}
            >

              <div style={dashboardCardStyle}>
                <h2 style={{ color: "#285c38", margin: 0 }}>
                  {recruiterResults?.total_uploaded ?? 0}
                </h2>
                <p style={{ color: "#686477", marginBottom: 0 }}>
                  Uploaded Resumes
                </p>
              </div>

              <div style={dashboardCardStyle}>
                <h2 style={{ color: "#285c38", margin: 0 }}>
                  {recruiterResults?.total_analyzed ?? 0}
                </h2>
                <p style={{ color: "#686477", marginBottom: 0 }}>
                  Analyzed Resumes
                </p>
              </div>

              <div style={dashboardCardStyle}>
                <h2 style={{ color: "#c05b3d", margin: 0 }}>
                  {recruiterResults?.total_failed ?? 0}
                </h2>
                <p style={{ color: "#686477", marginBottom: 0 }}>
                  Failed Resumes
                </p>
              </div>

            </div>

            {/* CANDIDATE RANKINGS */}
            <h2
              style={{
                color: "#211d35",
                marginBottom: "20px",
              }}
            >
              🏆 Candidate Rankings
            </h2>

            {candidateResults.length === 0 && (
              <div style={dashboardCardStyle}>
                No candidates were successfully analyzed.
              </div>
            )}

            {candidateResults.map((candidate, index) => {
              const score = Number(
                candidate.skill_match_score || 0
              );

              const matchedSkills =
                candidate.matched_skills || [];

              const missingSkills =
                candidate.missing_skills || [];

              return (
                <article
                  key={`${candidate.filename}-${index}`}
                  style={dashboardCardStyle}
                >

                  {/* RANK AND NAME */}
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      flexWrap: "wrap",
                      gap: "12px",
                    }}
                  >

                    <div>
                      <p
                        style={{
                          color: "#8b7b38",
                          fontSize: "12px",
                          fontWeight: "800",
                          letterSpacing: "1px",
                          margin: "0 0 8px",
                        }}
                      >
                        RANK #{candidate.rank ?? index + 1}
                      </p>

                      <h3
                        style={{
                          color: "#211d35",
                          margin: 0,
                          overflowWrap: "anywhere",
                        }}
                      >
                        📄 {candidate.filename}
                      </h3>

                      <p
                        style={{
                          color: "#686477",
                          fontSize: "13px",
                        }}
                      >
                        Status: {candidate.status || "Analyzed"}
                      </p>
                    </div>

                    <div
                      style={{
                        textAlign: "center",
                        minWidth: "105px",
                      }}
                    >
                      <h2
                        style={{
                          color: "#43885A",
                          fontSize: "32px",
                          margin: 0,
                        }}
                      >
                        {score.toFixed(0)}%
                      </h2>

                      <span
                        style={{
                          color: "#686477",
                          fontSize: "12px",
                        }}
                      >
                        Skill Match
                      </span>
                    </div>

                  </div>

                  {/* SKILL MATCH PROGRESS */}
                  <div
                    style={{
                      height: "9px",
                      background: "#e9eee8",
                      borderRadius: "20px",
                      overflow: "hidden",
                      margin: "14px 0",
                    }}
                  >
                    <div
                      style={{
                        height: "100%",
                        width: `${Math.max(0, Math.min(100, score))}%`,
                        background: "#43885A",
                        borderRadius: "20px",
                        transition: "width 0.4s ease",
                      }}
                    />
                  </div>

                  {/* SEMANTIC SCORE */}
                  <p
                    style={{
                      color: "#686477",
                      fontSize: "13px",
                    }}
                  >
                    Semantic Similarity:{" "}
                    <strong>
                      {candidate.semantic_similarity_score ?? 0}/100
                    </strong>
                  </p>

                  {/* MATCHING SKILLS */}
                  <div style={{ marginTop: "22px" }}>

                    <h4
                      style={{
                        color: "#285c38",
                        marginBottom: "10px",
                      }}
                    >
                      ✓ Matching Skills
                    </h4>

                    {matchedSkills.length > 0 ? (
                      <div
                        style={{
                          display: "flex",
                          flexWrap: "wrap",
                          gap: "9px",
                          marginTop: "10px",
                        }}
                      >
                        {matchedSkills.map((skill, skillIndex) => (
                          <span
                            key={`${skill}-${skillIndex}`}
                            style={skillStyle}
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p style={{ color: "#686477" }}>
                        No matching skills identified.
                      </p>
                    )}

                  </div>

                  {/* MISSING SKILLS */}
                  <div style={{ marginTop: "22px" }}>

                    <h4
                      style={{
                        color: "#a54b2b",
                        marginBottom: "10px",
                      }}
                    >
                      + Skills to Improve
                    </h4>

                    {missingSkills.length > 0 ? (
                      <div
                        style={{
                          display: "flex",
                          flexWrap: "wrap",
                          gap: "9px",
                          marginTop: "10px",
                        }}
                      >
                        {missingSkills.map((skill, skillIndex) => (
                          <span
                            key={`${skill}-${skillIndex}`}
                            style={missingSkillStyle}
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p
                        style={{
                          color: "#43885A",
                          fontWeight: "600",
                        }}
                      >
                        No missing skills identified.
                      </p>
                    )}

                  </div>

                  {/* SHORTLIST BUTTON */}
                  <div style={{ marginTop: "25px" }}>

                    <button
                      type="button"
                      className="primary-button"
                      disabled={Boolean(shortlistLoading[candidate.filename])}
                      onClick={() =>
                        handleShortlistCandidate(candidate)
                      }
                    >
                      {shortlistLoading[candidate.filename]
                        ? "Saving..."
                        : "✓ Shortlist Candidate"}
                    </button>

                    {shortlistMessages[candidate.filename] && (
                      <p
                        style={{
                          color: shortlistMessages[
                            candidate.filename
                          ].toLowerCase().includes("success")
                            ? "#43885A"
                            : "#c05b3d",
                          fontSize: "13px",
                          marginTop: "10px",
                        }}
                      >
                        {shortlistMessages[candidate.filename]}
                      </p>
                    )}

                  </div>

                </article>
              );
            })}

            {/* INVALID FILES */}
            {recruiterResults?.invalid_files?.length > 0 && (
              <section style={dashboardCardStyle}>

                <h3 style={{ color: "#a54b2b" }}>
                  Files That Could Not Be Analyzed
                </h3>

                {recruiterResults.invalid_files.map((file, index) => (
                  <p key={index} style={{ color: "#686477" }}>
                    {typeof file === "string"
                      ? file
                      : file.filename || JSON.stringify(file)}
                  </p>
                ))}

              </section>
            )}

            {/* SHORTLISTED CANDIDATES */}
            <section style={{ marginTop: "45px" }}>

              <h2
                style={{
                  color: "#211d35",
                  marginBottom: "8px",
                }}
              >
                ⭐ Shortlisted Candidates
              </h2>

              <p
                style={{
                  color: "#686477",
                  marginBottom: "20px",
                }}
              >
                Candidates saved through the backend shortlist feature.
              </p>

              <div style={dashboardCardStyle}>

                <h3 style={{ color: "#285c38", marginTop: 0 }}>
                  Total Shortlisted: {shortlistedCandidates.length}
                </h3>

                {shortlistedCandidates.length === 0 ? (
                  <p style={{ color: "#686477" }}>
                    No candidates have been shortlisted yet.
                  </p>
                ) : (
                  shortlistedCandidates.map((candidate) => (
                    <div
                      key={candidate.id}
                      style={{
                        padding: "16px 0",
                        borderBottom: "1px solid #eeebf5",
                      }}
                    >

                      <strong
                        style={{
                          color: "#211d35",
                          overflowWrap: "anywhere",
                        }}
                      >
                        {candidate.filename}
                      </strong>

                      <p
                        style={{
                          color: "#686477",
                          fontSize: "13px",
                          margin: "7px 0",
                        }}
                      >
                        Skill Match:{" "}
                        {Number(
                          candidate.skill_match_score || 0
                        ).toFixed(0)}%
                      </p>

                      <span
                        style={{
                          color: "#43885A",
                          fontSize: "12px",
                          fontWeight: "700",
                        }}
                      >
                        {candidate.status || "Shortlisted"}
                      </span>

                    </div>
                  ))
                )}

              </div>

              <button
                className="primary-button"
                type="button"
                onClick={() => {
                  navigateTo("recruiter");
                  setRecruiterResults(null);
                  sessionStorage.removeItem("hirematch_recruiter_results");
                  setShortlistMessages({});
                }}
              >
                Analyze More Candidates →
              </button>

            </section>

          </div>
        </main>
      )}

      {/* FOOTER */}
      <footer className="footer">

        <button
          className="brand footer-brand"
          onClick={() => navigateTo("home")}
        >
          HireMatch<span>.AI</span>
        </button>

        <p>Connecting people with possibilities.</p>

        <small>
          © 2026 HireMatch-AI · Built for better career connections
        </small>

      </footer>

    </div>
  );
}

// BROWSER ROUTER
export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}