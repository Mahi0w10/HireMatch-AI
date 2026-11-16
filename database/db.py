
import sqlite3
import json
from pathlib import Path

# Database path
DB_DIR = Path(__file__).resolve().parent
DB_PATH = DB_DIR / "hirematch.db"


def get_db_connection():
    """Create a SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the required database tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

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


def save_analysis(filename, job_description, skill_match_score,
                  semantic_similarity_score, matched_skills,
                  missing_skills, rank=None):

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO analysis_results
            (filename, job_description, skill_match_score,
             semantic_similarity_score, matched_skills,
             missing_skills, rank)
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


def shortlist_candidate(filename, job_description,
                        skill_match_score, notes=""):

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO shortlists
            (filename, job_description, skill_match_score, notes)
            VALUES (?, ?, ?, ?)
        """, (
            filename,
            job_description,
            skill_match_score,
            notes
        ))

        conn.commit()
        return cursor.lastrowid


def get_shortlisted_candidates():

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, filename, job_description,
                   skill_match_score, status, notes,
                   shortlisted_at
            FROM shortlists
            ORDER BY shortlisted_at DESC
        """)

        return [dict(row) for row in cursor.fetchall()]


# Initialize tables automatically
init_db()
