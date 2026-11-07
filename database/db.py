import sqlite3
import json
from pathlib import Path

# Database path setup
DB_DIR = Path("database")
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "hirematch.db"


def get_db_connection():
    """Returns a SQLite connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database and creates required tables if they don't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Table for analysis records
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                job_description TEXT NOT NULL,
                skill_match_score REAL,
                semantic_similarity_score INTEGER NOT NULL,
                matched_skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                rank INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Table for recruiter shortlisted candidates
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shortlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                job_description TEXT NOT NULL,
                skill_match_score REAL,
                status TEXT DEFAULT 'Shortlisted',
                notes TEXT,
                shortlisted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_analysis(filename, job_description, skill_match_score, semantic_similarity_score, matched_skills, missing_skills, rank=None):
    """Saves candidate evaluation to analysis_results table."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_results 
            (filename, job_description, skill_match_score, semantic_similarity_score, matched_skills, missing_skills, rank)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            job_description,
            skill_match_score,
            semantic_similarity_score,
            json.dumps(matched_skills),
            json.dumps(missing_skills),
            rank
        ))
        conn.commit()
        return cursor.lastrowid


def shortlist_candidate(filename, job_description, skill_match_score, notes=""):
    """Saves or updates a candidate in the shortlists table."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO shortlists (filename, job_description, skill_match_score, notes)
            VALUES (?, ?, ?, ?)
        """, (filename, job_description, skill_match_score, notes))
        conn.commit()
        return cursor.lastrowid


def get_shortlisted_candidates():
    """Retrieves all shortlisted candidates ordered by latest shortlist date."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, filename, job_description, skill_match_score, status, notes, shortlisted_at
            FROM shortlists
            ORDER BY shortlisted_at DESC
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


# Auto-initialize database tables on import
init_db()
