
import React, { useState } from "react";
import "./App.css";

export default function App() {
  const [page, setPage] = useState("home");
  
const [selectedResume, setSelectedResume] = useState(null);
const [resumeError, setResumeError] = useState("");
  return (
    <div className="app">
      <nav className="navbar">
        <button className="brand" onClick={() => setPage("home")}>
          HireMatch<span>.AI</span>
        </button>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
        </div>

        <button className="nav-button" onClick={() => setPage("recruiter")}>
          Recruiter Portal ↗
        </button>
      </nav>

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
              Meet your smarter hiring companion. Match skills, discover
              opportunities, and make better career decisions with AI.
            </p>

            <div className="role-grid">
              <button
                className="role-card seeker-card"
                onClick={() => setPage("seeker")}
              >
                <span className="role-icon">💼</span>
                <span className="role-label">FOR JOB SEEKERS</span>
                <strong>Find your perfect match</strong>
                <span className="role-description">
                  Upload your resume and discover how well you fit a job.
                </span>
                <span className="role-link">Check my match <span>→</span></span>
              </button>

              <button
                className="role-card recruiter-card"
                onClick={() => setPage("recruiter")}
              >
                <span className="role-icon">🤝</span>
                <span className="role-label">FOR RECRUITERS</span>
                <strong>Discover exceptional talent</strong>
                <span className="role-description">
                  Create job listings and rank candidates by their skills.
                </span>
                <span className="role-link">Find talent <span>→</span></span>
              </button>
            </div>

            <div className="trust-line">
              <span>✳</span> Smarter matching. More meaningful careers.
            </div>
          </main>

          <section className="features-section" id="features">
            <div className="section-kicker">BUILT FOR BOTH SIDES</div>
            <h2>One platform. Better matches.</h2>
            <p className="section-description">
              Everything you need to make the next professional connection.
            </p>

            <div className="features-grid">
              <article className="feature-card">
                <div className="feature-icon">📄</div>
                <h3>Resume insights</h3>
                <p>Understand how your experience aligns with job requirements.</p>
              </article>

              <article className="feature-card">
                <div className="feature-icon">🎯</div>
                <h3>Skill matching</h3>
                <p>Focus on relevant skills and identify areas to improve.</p>
              </article>

              <article className="feature-card">
                <div className="feature-icon">📊</div>
                <h3>Candidate ranking</h3>
                <p>Help recruiters organise candidates against a job's needs.</p>
              </article>
            </div>
          </section>

          <section className="how-section" id="how-it-works">
            <div className="section-kicker">SIMPLE BY DESIGN</div>
            <h2>Your next step, made simpler.</h2>
            <div className="steps-grid">
              <div className="step-card">
                <span>01</span>
                <h3>Share your details</h3>
                <p>Upload a resume or describe the role you need to fill.</p>
              </div>
              <div className="step-card">
                <span>02</span>
                <h3>Compare skills</h3>
                <p>Review the information against the job requirements.</p>
              </div>
              <div className="step-card">
                <span>03</span>
                <h3>Move forward</h3>
                <p>Use the insights to guide your next hiring or career step.</p>
              </div>
            </div>
          </section>
        </>
      )}

      {page === "seeker" && (
        <main className="workspace">
          <button className="back-button" onClick={() => setPage("home")}>
            ← Back to home
          </button>

          <div className="section-kicker">JOB SEEKER WORKSPACE</div>
          <h1>Find your <span>best match.</span></h1>
          <p className="workspace-description">
            Add your resume and the job description you want to explore.
          </p>

          <form
  className="workspace-form"
 onSubmit={(event) => {
  event.preventDefault();
  setPage("results");
}}
>
            <label htmlFor="resume">Upload your resume (PDF or DOCX)</label>
            
<input
  id="resume"
  type="file"
  accept=".pdf,.doc,.docx"
  required
  onChange={(event) => {
    const file = event.target.files[0];
    setResumeError("");
    setSelectedResume(null);

    if (!file) return;

    const allowedTypes = [".pdf", ".doc", ".docx"];
    const extension = file.name
      .slice(file.name.lastIndexOf("."))
      .toLowerCase();

    if (!allowedTypes.includes(extension)) {
      setResumeError("Please upload a PDF, DOC, or DOCX file.");
      event.target.value = "";
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setResumeError("Resume size must be 10 MB or less.");
      event.target.value = "";
      return;
    }

    setSelectedResume(file);
  }}
/>

{resumeError && (
  <p className="form-error">{resumeError}</p>
)}

{selectedResume && (
  <p className="form-success">
    Selected resume: {selectedResume.name}
  </p>
)}


            <label htmlFor="job-description">Job description</label>
            
<textarea
  id="job-description"
  rows="7"
  placeholder="Paste the job description here, including required skills, experience, and responsibilities..."
  minLength={30}
  maxLength={5000}
  required
/>
<p className="form-note">
  Include the job responsibilities, required skills, and experience.
  (30–5000 characters)
</p>


            <button className="primary-button" type="submit">
              Prepare My Match →
            </button>
            <p className="form-note">
              AI scoring will need to be connected to the backend.
            </p>
          </form>
        </main>
      )}

{page === "results" && (
  <main className="workspace">
    <button
      className="back-button"
      onClick={() => setPage("seeker")}
    >
      ← Back to form
    </button>

    <div className="section-kicker">MATCH RESULTS · DEMO</div>
    <h1>Your career <span>match report.</span></h1>

    <p className="workspace-description">
      This is a sample preview. Actual AI matching is not connected yet.
    </p>

    <div className="features-grid">
      <article className="feature-card">
        <div className="feature-icon">🎯</div>
        <h3>Match score</h3>
        <p>78% sample score — not calculated from your resume.</p>
      </article>

     
<article className="feature-card score-card">
  <div className="feature-icon">🎯</div>
  <h3>Match score</h3>

  <div className="score-circle">
    <svg viewBox="0 0 160 160" className="score-ring">
      <circle
        className="score-ring-bg"
        cx="80"
        cy="80"
        r="68"
      />
      <circle
        className="score-ring-progress"
        cx="80"
        cy="80"
        r="68"
      />
    </svg>
    <div className="score-value">78%</div>
  </div>

  <p>Sample score — actual AI matching is not connected yet.</p>
</article>


      <article className="feature-card">
        <div className="feature-icon">📈</div>
        <h3>Skills to improve</h3>
        <p>Suggestions will appear here after analysis is connected.</p>
      </article>
    </div>
  </main>
)}

      {page === "recruiter" && (
        <main className="workspace">
          <button className="back-button" onClick={() => setPage("home")}>
            ← Back to home
          </button>

          <div className="section-kicker">RECRUITER WORKSPACE</div>
          <h1>Build your <span>dream team.</span></h1>
          <p className="workspace-description">
            Create a job listing and add candidate resumes for review.
          </p>

          <form className="workspace-form" onSubmit={(event) => {
            event.preventDefault();
            alert("Your job details are ready for the next backend integration step.");
          }}>
            <label htmlFor="job-title">Job title</label>
            <input
              id="job-title"
              type="text"
              placeholder="e.g. Frontend Developer"
              required
            />

            <label htmlFor="job-details">Job description and required skills</label>
            <textarea
              id="job-details"
              rows="5"
              placeholder="Describe the role, responsibilities, and required skills..."
              required
            />

            <label htmlFor="candidate-resumes">Upload candidate resumes (PDF or DOCX)</label>
            <input
              id="candidate-resumes"
              type="file"
              accept=".pdf,.doc,.docx"
              multiple
              required
            />

            <button className="primary-button" type="submit">
              Prepare Candidate Review →
            </button>
            <p className="form-note">
              Candidate ranking will need to be connected to the backend.
            </p>
          </form>
        </main>
      )}

      <footer className="footer">
        <button className="brand footer-brand" onClick={() => setPage("home")}>
          HireMatch<span>.AI</span>
        </button>
        <p>Connecting people with possibilities.</p>
        <small>© 2026 HireMatch-AI · Built for better career connections</small>
      </footer>
    </div>
  );
}
