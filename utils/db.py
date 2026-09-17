"""
Database management for projects and data points.
Uses SQLite for MVP (easy migration to PostgreSQL later).
"""
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/dancarbon.db")


def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            gas TEXT NOT NULL,
            solvent TEXT NOT NULL,
            nanoparticle TEXT,
            owner_email TEXT,
            status TEXT DEFAULT 'collecting',
            min_points INTEGER DEFAULT 15,
            model_r2 REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS data_points (
            point_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            pressure REAL,
            temperature REAL,
            concentration REAL,
            absorption REAL,
            source TEXT DEFAULT 'manual',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (project_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS contributions (
            contrib_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            contribution_type TEXT,
            source TEXT,
            email TEXT,
            ai_score REAL,
            status TEXT DEFAULT 'pending',
            extracted_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_project(name, gas, solvent, nanoparticle, owner_email=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO projects (project_name, gas, solvent, nanoparticle, owner_email)
        VALUES (?, ?, ?, ?, ?)
    """, (name, gas, solvent, nanoparticle, owner_email))
    conn.commit()
    project_id = c.lastrowid
    conn.close()
    return project_id


def list_projects():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM projects ORDER BY created_at DESC", conn)
    conn.close()
    return df


def get_project(project_id):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM projects WHERE project_id = ?",
        conn, params=(project_id,)
    )
    conn.close()
    return df.iloc[0] if len(df) > 0 else None


def add_data_point(project_id, pressure, temperature, concentration, absorption,
                   source='manual', notes=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO data_points
        (project_id, pressure, temperature, concentration, absorption, source, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (project_id, pressure, temperature, concentration, absorption, source, notes))
    conn.commit()
    conn.close()


def get_project_data(project_id):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM data_points WHERE project_id = ? ORDER BY created_at",
        conn, params=(project_id,)
    )
    conn.close()
    return df


def update_project_status(project_id, status, model_r2=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if model_r2 is not None:
        c.execute("""
            UPDATE projects SET status = ?, model_r2 = ?
            WHERE project_id = ?
        """, (status, model_r2, project_id))
    else:
        c.execute("UPDATE projects SET status = ? WHERE project_id = ?",
                  (status, project_id))
    conn.commit()
    conn.close()


def add_contribution(title, description, ctype, source, email, ai_score, status='pending'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO contributions
        (title, description, contribution_type, source, email, ai_score, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, ctype, source, email, ai_score, status))
    conn.commit()
    conn.close()


def list_contributions(status=None):
    conn = sqlite3.connect(DB_PATH)
    if status:
        df = pd.read_sql_query(
            "SELECT * FROM contributions WHERE status = ? ORDER BY created_at DESC",
            conn, params=(status,)
        )
    else:
        df = pd.read_sql_query(
            "SELECT * FROM contributions ORDER BY created_at DESC", conn
        )
    conn.close()
    return df


# Initialize on import
init_db()
