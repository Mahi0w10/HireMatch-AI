
import './Results.css'

function Results() {
  return (
    <div className="results-page">
      <nav className="results-navbar">
        <a className="results-brand" href="/">
          <span className="results-brand-icon">H</span>
          HireMatch<span className="results-brand-ai">.AI</span>
        </a>

        <a className="back-button" href="/">
          ← Back to Home
        </a>
      </nav>

      <main className="results-main">
        <div className="results-heading">
          <span className="results-eyebrow">YOUR ANALYSIS</span>
          <h1>Your Match Results</h1>
          <p>Here is how your resume aligns with the job description.</p>
        </div>

        <section className="score-card">
          <div className="score-circle">
            <div>
              <strong>85%</strong>
              <span>Match score</span>
            </div>
          </div>

          <div className="score-details">
            <span className="score-badge">Strong potential</span>
            <h2>You’re off to a great start!</h2>
            <p>
              Your resume shows a good alignment with this role.
              Review the skills below to identify areas for improvement.
            </p>
          </div>
        </section>

        <div className="results-grid">
          <section className="skills-card">
            <h2>✓ Matching Skills</h2>
            <p>Skills that align with the job requirements.</p>
            <div className="skill-list">
              <span>React</span>
              <span>JavaScript</span>
              <span>HTML & CSS</span>
              <span>Communication</span>
            </div>
          </section>

          <section className="skills-card missing-card">
            <h2>＋ Skills to Improve</h2>
            <p>Skills you could highlight or develop further.</p>
            <div className="skill-list">
              <span>TypeScript</span>
              <span>Testing</span>
              <span>REST APIs</span>
            </div>
          </section>
        </div>

        <section className="suggestions-card">
          <span className="results-eyebrow">NEXT STEPS</span>
          <h2>Suggestions to improve your resume</h2>

          <div className="suggestion-item">
            <span>01</span>
            <p>Highlight relevant projects that demonstrate your skills.</p>
          </div>

          <div className="suggestion-item">
            <span>02</span>
            <p>Include important job-related keywords where accurate.</p>
          </div>

          <div className="suggestion-item">
            <span>03</span>
            <p>Add measurable achievements to your experience section.</p>
          </div>
        </section>

        <a className="results-home-button" href="/">
          Back to Home →
        </a>

        <p className="demo-note">
          Demo results only — actual AI analysis will be connected later.
        </p>
      </main>
    </div>
  )
}

export default Results
