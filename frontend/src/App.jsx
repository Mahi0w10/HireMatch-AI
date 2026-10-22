import './App.css'

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <a className="brand" href="#">
          <span className="brand-icon">H</span>
          HireMatch<span className="brand-ai">.AI</span>
        </a>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>
        </div>

        <a className="nav-button" href="#get-started">
          Get Started <span>↗</span>
        </a>
      </nav>

      <main>
        <section className="hero">
          <div className="announcement">
            <span className="status-dot"></span>
            AI-powered resume matching
          </div>

          <h1>
            Your next opportunity,
            <br />
            <span>matched intelligently.</span>
          </h1>

          <p className="hero-description">
            Find out how well your resume fits a job. Get insights into your
            skills, discover missing keywords, and take the next step in your
            career with confidence.
          </p>

          <a className="primary-button" href="#get-started">
            Match My Resume <span>→</span>
          </a>

          <div className="trust-note">
            <span>✓</span> Simple, smart, and career-focused
          </div>
        </section>

        <section className="match-card" id="get-started">
          <div className="card-heading">
            <div>
              <span className="eyebrow">GET STARTED</span>
              <h2>Check your job match</h2>
              <p>Provide your resume and the job description below.</p>
            </div>
            <div className="card-icon">✦</div>
          </div>

          <form onSubmit={(event) => {
            event.preventDefault()
            console.log('Resume form submitted')
          }}>
            <label htmlFor="resume">Your resume</label>
            <div className="upload-area">
              <span className="upload-icon">↑</span>
              <div>
                <label className="upload-label" htmlFor="resume">
                  Choose a resume file
                </label>
                <p>PDF or DOCX format</p>
              </div>
              <input
                id="resume"
                type="file"
                accept=".pdf,.doc,.docx"
                required
              />
            </div>

            <label htmlFor="job-description">Job description</label>
            <textarea
              id="job-description"
              placeholder="Paste the job description here..."
              rows="5"
              required
            ></textarea>

            <button className="submit-button" type="submit">
              Analyze My Match <span>→</span>
            </button>
            <p className="privacy-note">
              Your career journey starts with a better match.
            </p>
          </form>
        </section>

        <section className="features" id="features">
          <div className="section-heading">
            <span className="eyebrow">WHY HIREMATCH AI?</span>
            <h2>A smarter way to apply.</h2>
          </div>

          <div className="feature-grid">
            <article className="feature-card">
              <div className="feature-icon purple">◎</div>
              <h3>Match insights</h3>
              <p>Understand how your resume aligns with a job's requirements.</p>
            </article>

            <article className="feature-card">
              <div className="feature-icon green">✧</div>
              <h3>Skill gap awareness</h3>
              <p>Identify skills and keywords you may need to highlight.</p>
            </article>

            <article className="feature-card">
              <div className="feature-icon orange">↗</div>
              <h3>Apply with confidence</h3>
              <p>Use actionable insights to improve your job applications.</p>
            </article>
          </div>
        </section>

        <section className="how-section" id="how-it-works">
          <span className="eyebrow">HOW IT WORKS</span>
          <h2>Three simple steps.</h2>
          <p>Upload your resume, add a job description, and review your match insights.</p>
        </section>
      </main>

      <footer>
        <a className="brand footer-brand" href="#">
          <span className="brand-icon">H</span>
          HireMatch<span className="brand-ai">.AI</span>
        </a>
        <p>Helping you find your next opportunity.</p>
      </footer>
    </div>
  )
}

export default App