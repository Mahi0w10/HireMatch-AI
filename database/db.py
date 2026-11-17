import sqlite3
import json
from database.connection import get_connection

def init_db():
    """Initializes the database using Tanishka's connection and creates required tables."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
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
    conn.close()


def save_analysis(filename, job_description, skill_match_score, semantic_similarity_score, matched_skills, missing_skills, rank=None):
    """Saves candidate evaluation to analysis_results table."""
    conn = get_connection()
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
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def shortlist_candidate(filename, job_description, skill_match_score, notes=""):
    """Saves or updates a candidate in the shortlists table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO shortlists (filename, job_description, skill_match_score, notes)
        VALUES (?, ?, ?, ?)
    """, (filename, job_description, skill_match_score, notes))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def get_shortlisted_candidates():
    """Retrieves all shortlisted candidates ordered by latest shortlist date."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, filename, job_description, skill_match_score, status, notes, shortlisted_at
        FROM shortlists
        ORDER BY shortlisted_at DESC
    """)
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result

# Auto-initialize database tables on import
init_db()
