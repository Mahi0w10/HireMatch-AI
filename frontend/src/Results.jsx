
import "./Results.css";

function Results({ onBack, resumeName, jobDescription }) {
  return (
    <div className="results-page">

      {/* NAVBAR */}
      <nav className="results-navbar">
        <button
          className="results-brand"
          type="button"
          onClick={onBack}
        >
          <span className="results-brand-icon">H</span>
          HireMatch
          <span className="results-brand-ai">.AI</span>
        </button>

        <button
          className="back-button"
          type="button"
          onClick={onBack}
        >
          ← Back to Form
        </button>
      </nav>

      <main className="results-main">

        {/* HEADING */}
        <div className="results-heading">
          <span className="results-eyebrow">
            YOUR ANALYSIS · DEMO
          </span>
          <h1>Your Match Results</h1>
          <p>
            Here is how your resume aligns with the job description.
          </p>
        </div>

        {/* UPLOADED RESUME */}
        <section className="skills-card">
          <h2>📄 Uploaded Resume</h2>
          <p>{resumeName || "No resume selected"}</p>
        </section>

        {/* JOB DESCRIPTION */}
        <section className="skills-card">
          <h2>💼 Job Description</h2>
          <p className="job-description-preview">
            {jobDescription || "No job description provided."}
          </p>
        </section>

        {/* MATCH SCORE - DEMO */}
        <section className="score-card">
          <div className="score-circle">
            <div>
              <strong>85%</strong>
              <span>Demo score</span>
            </div>
          </div>

          <div className="score-details">
            <span className="score-badge">
              Sample result
            </span>
            <h2>You’re off to a great start!</h2>
            <p>
              This is a sample match score. Actual resume
              analysis will be performed after backend integration.
            </p>
          </div>
        </section>

        {/* SKILLS SECTION */}
        <div className="results-grid">

          <section className="skills-card">
            <h2>✓ Matching Skills</h2>
            <p>Sample matching skills.</p>
            <div className="skill-list">
              <span>Python</span>
              <span>SQL</span>
              <span>Excel</span>
              <span>Data Analysis</span>
            </div>
          </section>

          <section className="skills-card missing-card">
            <h2>＋ Skills to Improve</h2>
            <p>Sample skills to develop further.</p>
            <div className="skill-list">
              <span>Power BI</span>
              <span>Statistics</span>
              <span>Tableau</span>
            </div>
          </section>

        </div>

        {/* SUGGESTIONS */}
        <section className="suggestions-card">
          <span className="results-eyebrow">NEXT STEPS</span>
          <h2>Suggestions to improve your resume</h2>

          <div className="suggestion-item">
            <span>01</span>
            <p>
              Highlight relevant data analysis projects.
            </p>
          </div>

          <div className="suggestion-item">
            <span>02</span>
            <p>
              Include Python, SQL, and Excel skills where accurate.
            </p>
          </div>

          <div className="suggestion-item">
            <span>03</span>
            <p>
              Add measurable achievements to your projects.
            </p>
          </div>
        </section>

        <button
          className="results-home-button"
          type="button"
          onClick={onBack}
        >
          ← Back to Form
        </button>

        <p className="demo-note">
          Demo results only — actual AI analysis will be connected later.
        </p>

      </main>
    </div>
  );
}

export default Results;
