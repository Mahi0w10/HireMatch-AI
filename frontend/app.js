const API_BASE = "";

function switchTab(tab) {
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

  if (tab === "seeker") {
    document.getElementById("btn-tab-seeker").classList.add("active");
    document.getElementById("seeker-tab").classList.add("active");
  } else if (tab === "recruiter") {
    document.getElementById("btn-tab-recruiter").classList.add("active");
    document.getElementById("recruiter-tab").classList.add("active");
  } else if (tab === "shortlist") {
    document.getElementById("btn-tab-shortlist").classList.add("active");
    document.getElementById("shortlist-tab").classList.add("active");
    loadShortlisted();
  }
}

// 1. Single Resume Analysis
async function handleSingleAnalyze(e) {
  e.preventDefault();
  const fileInput = document.getElementById("single-resume");
  const jdInput = document.getElementById("single-jd");
  const btn = document.getElementById("single-btn");

  if (!fileInput.files.length) return alert("Please select a PDF resume!");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("job_description", jdInput.value);

  btn.disabled = true;
  btn.querySelector(".btn-text").textContent = "Analyzing Resume...";

  try {
    const res = await fetch(`${API_BASE}/analyze-resume`, {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Analysis failed");

    const a = data.analysis;
    document.getElementById("res-skill-score").textContent = a.skill_match_score !== null ? `${a.skill_match_score}%` : "N/A";
    document.getElementById("res-semantic-score").textContent = `${a.semantic_similarity_score}/100`;

    // Render tags
    const matchedBox = document.getElementById("res-matched-skills");
    matchedBox.innerHTML = a.matched_skills.length 
      ? a.matched_skills.map(s => `<span class="tag tag-matched">${s}</span>`).join("")
      : "<em>No required skills matched</em>";

    const missingBox = document.getElementById("res-missing-skills");
    missingBox.innerHTML = a.missing_skills.length
      ? a.missing_skills.map(s => `<span class="tag tag-missing">${s}</span>`).join("")
      : "<em>None! Perfect match.</em>";

    const suggList = document.getElementById("res-suggestions");
    suggList.innerHTML = a.suggestions.map(s => `<li>${s}</li>`).join("");

    document.getElementById("single-result-box").style.display = "block";
  } catch (err) {
    alert("Error: " + err.message);
  } finally {
    btn.disabled = false;
    btn.querySelector(".btn-text").textContent = "Analyze Resume";
  }
}

// 2. Batch Resume Screening
let currentBatchJD = "";
async function handleBatchAnalyze(e) {
  e.preventDefault();
  const filesInput = document.getElementById("batch-resumes");
  const jdInput = document.getElementById("batch-jd");
  const btn = document.getElementById("batch-btn");

  if (!filesInput.files.length) return alert("Select at least 1 PDF resume!");
  currentBatchJD = jdInput.value;

  const formData = new FormData();
  for (let file of filesInput.files) {
    formData.append("files", file);
  }
  formData.append("job_description", currentBatchJD);

  btn.disabled = true;
  btn.querySelector(".btn-text").textContent = "Ranking Candidates...";

  try {
    const res = await fetch(`${API_BASE}/analyze-multiple-resumes`, {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Batch analysis failed");

    const tbody = document.getElementById("ranked-tbody");
    tbody.innerHTML = "";

    data.results.forEach(cand => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><span class="rank-badge">${cand.rank || "-"}</span></td>
        <td><strong>${cand.filename}</strong></td>
        <td>${cand.skill_match_score !== null ? cand.skill_match_score + "%" : "N/A"}</td>
        <td>${cand.semantic_similarity_score !== null ? cand.semantic_similarity_score + "/100" : "N/A"}</td>
        <td>${cand.matched_skills.map(s => `<span class="tag tag-matched">${s}</span>`).join(" ")}</td>
        <td>${cand.missing_skills.map(s => `<span class="tag tag-missing">${s}</span>`).join(" ")}</td>
        <td>
          ${cand.status === "Analyzed" 
            ? `<button class="btn btn-sm btn-success" onclick="shortlistCandidate('${cand.filename}', ${cand.skill_match_score}, this)">Shortlist</button>`
            : `<span class="tag tag-missing">${cand.status}</span>`
          }
        </td>
      `;
      tbody.appendChild(tr);
    });

    document.getElementById("batch-result-container").style.display = "block";
  } catch (err) {
    alert("Error: " + err.message);
  } finally {
    btn.disabled = false;
    btn.querySelector(".btn-text").textContent = "Screen & Rank Candidates";
  }
}

// 3. Shortlist Action
async function shortlistCandidate(filename, score, btn) {
  btn.disabled = true;
  btn.textContent = "Saving...";

  try {
    const res = await fetch(`${API_BASE}/shortlist-candidate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: filename,
        job_description: currentBatchJD || "General Role",
        skill_match_score: score,
        notes: "Shortlisted from Recruiter Dashboard"
      })
    });
    if (!res.ok) throw new Error("Failed to shortlist");
    btn.className = "btn btn-sm btn-secondary";
    btn.textContent = "Shortlisted ✓";
  } catch (err) {
    alert("Error: " + err.message);
    btn.disabled = false;
    btn.textContent = "Shortlist";
  }
}

// 4. Load Shortlisted Candidates
async function loadShortlisted() {
  const tbody = document.getElementById("shortlist-tbody");
  tbody.innerHTML = "<tr><td colspan='7'>Loading shortlisted candidates...</td></tr>";

  try {
    const res = await fetch(`${API_BASE}/shortlisted-candidates`);
    const data = await res.json();
    tbody.innerHTML = "";

    if (!data.candidates.length) {
      tbody.innerHTML = "<tr><td colspan='7'>No candidates shortlisted yet.</td></tr>";
      return;
    }

    data.candidates.forEach(c => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${c.id}</td>
        <td><strong>${c.filename}</strong></td>
        <td>${c.job_description.substring(0, 50)}...</td>
        <td>${c.skill_match_score !== null ? c.skill_match_score + "%" : "N/A"}</td>
        <td><span class="tag tag-matched">${c.status}</span></td>
        <td>${c.notes || "-"}</td>
        <td>${c.shortlisted_at}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan='7'>Error loading: ${err.message}</td></tr>`;
  }
}
