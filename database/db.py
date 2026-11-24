import json
import sqlite3
from database.connection import get_connection

def init_db():
    """Initialize the database and create required tables."""
    conn = get_connection()
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
    conn.close()


def shortlist_candidate(
    filename,
    job_description,
    skill_match_score,
    notes=""
):
    """
    Updates an existing shortlist record instead of
    creating duplicate records for the same candidate and job.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id
            FROM shortlists
            WHERE LOWER(TRIM(filename)) = LOWER(TRIM(?))
              AND LOWER(TRIM(job_description)) = LOWER(TRIM(?))
            ORDER BY id DESC
            LIMIT 1
        """, (filename, job_description))

        existing = cursor.fetchone()

        if existing:
            record_id = existing[0]

            cursor.execute("""
                UPDATE shortlists
                SET skill_match_score = ?,
                    notes = ?,
                    status = 'Shortlisted',
                    shortlisted_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (skill_match_score, notes, record_id))

            cursor.execute("""
                DELETE FROM shortlists
                WHERE LOWER(TRIM(filename)) = LOWER(TRIM(?))
                  AND LOWER(TRIM(job_description)) = LOWER(TRIM(?))
                  AND id != ?
            """, (filename, job_description, record_id))

        else:
            cursor.execute("""
                INSERT INTO shortlists (
                    filename,
                    job_description,
                    skill_match_score,
                    notes
                )
                VALUES (?, ?, ?, ?)
            """, (filename, job_description, skill_match_score, notes))

            record_id = cursor.lastrowid

        conn.commit()
        return record_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def get_shortlisted_candidates():
    """Retrieve all shortlisted candidates, newest first."""

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                id,
                filename,
                job_description,
                skill_match_score,
                status,
                notes,
                shortlisted_at
            FROM shortlists
            ORDER BY shortlisted_at DESC, id DESC
        """)

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    finally:
        conn.close()

def save_analysis(
    filename,
    job_description,
    skill_match_score,
    semantic_similarity_score,
    matched_skills,
    missing_skills,
    rank=None
):
    """Save resume analysis results in SQLite database."""

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO analysis_results (
                filename,
                job_description,
                skill_match_score,
                semantic_similarity_score,
                matched_skills,
                missing_skills,
                rank
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            job_description,
            skill_match_score,
            semantic_similarity_score,
            json.dumps(matched_skills or []),
            json.dumps(missing_skills or []),
            rank
        ))

        record_id = cursor.lastrowid
        conn.commit()
        return record_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

# Auto-initialize database tables on import
init_db()
