
import "./Results.css";

function Results({ onBack, resumeName, jobDescription, analysis }) {
  const score = analysis?.skill_match_score ?? 0;
  const semanticScore = analysis?.semantic_similarity_score;
  const matchedSkills = analysis?.matched_skills ?? [];
  const missingSkills = analysis?.missing_skills ?? [];
  const suggestions = analysis?.suggestions ?? [];

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
            YOUR ANALYSIS · AI POWERED
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

        {/* ACTUAL MATCH SCORE */}
        <section className="score-card">

          <div
  className="score-circle"
  style={{ "--score": score }}
>
            <div>
              <strong>{score}%</strong>
              <span>Skill match</span>
            </div>
          </div>

          <div className="score-details">

            <span className="score-badge">
              Analysis completed
            </span>

            <h2>
              {score >= 75
                ? "Great match!"
                : score >= 50
                ? "Good starting point!"
                : "Room for improvement!"}
            </h2>

            <p>
              Your resume matches {score}% of the identified
              required skills.
            </p>

            {semanticScore !== undefined && (
              <p>
                Semantic similarity score: {semanticScore}/100
              </p>
            )}

          </div>
        </section>

        {/* SKILLS SECTION */}
        <div className="results-grid">

          {/* MATCHING SKILLS */}
          <section className="skills-card">

            <h2>✓ Matching Skills</h2>

            <p>Skills found in your resume.</p>

            <div className="skill-list">
              {matchedSkills.length > 0 ? (
                matchedSkills.map((skill, index) => (
                  <span key={index}>{skill}</span>
                ))
              ) : (
                <p>No matching skills found.</p>
              )}
            </div>

          </section>

          {/* MISSING SKILLS */}
          <section className="skills-card missing-card">

            <h2>＋ Skills to Improve</h2>

            <p>Required skills not found in your resume.</p>

            <div className="skill-list">
              {missingSkills.length > 0 ? (
                missingSkills.map((skill, index) => (
                  <span key={index}>{skill}</span>
                ))
              ) : (
                <p>No missing skills identified.</p>
              )}
            </div>

          </section>

        </div>

        {/* SUGGESTIONS */}
        <section className="suggestions-card">

          <span className="results-eyebrow">
            NEXT STEPS
          </span>

          <h2>Suggestions to improve your resume</h2>

          {suggestions.length > 0 ? (
            suggestions.map((suggestion, index) => (
              <div className="suggestion-item" key={index}>
                <span>
                  {String(index + 1).padStart(2, "0")}
                </span>

                <p>{suggestion}</p>
              </div>
            ))
          ) : (
            <p>No additional suggestions available.</p>
          )}

        </section>

        {/* BACK BUTTON */}
        <button
          className="results-home-button"
          type="button"
          onClick={onBack}
        >
          ← Back to Form
        </button>

        <p className="demo-note">
          Results generated using the HireMatch AI backend.
        </p>

      </main>
    </div>
  );
}

export default Results;
