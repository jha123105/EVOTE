"""
Database initialization and sample data seeding.
Creates tables and inserts default positions/candidates if empty.
"""
import sqlite3

DB_NAME = "evote.db"


def get_connection():
    """Create and return a database connection with row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """
    Create all required tables and insert sample data if the database is empty.
    Only runs table creation if tables don't exist - never drops existing data.
    """
    conn = get_connection()
    cursor = conn.cursor()

    #  Create Tables 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            position_id INTEGER NOT NULL,
            image_path TEXT DEFAULT NULL,
            votes INTEGER DEFAULT 0,
            FOREIGN KEY(position_id) REFERENCES positions(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voters (
            email TEXT PRIMARY KEY,
            has_voted INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_email TEXT NOT NULL,
            candidate_id INTEGER NOT NULL,
            position_id INTEGER NOT NULL,
            FOREIGN KEY(voter_email) REFERENCES voters(email),
            FOREIGN KEY(candidate_id) REFERENCES candidates(id),
            FOREIGN KEY(position_id) REFERENCES positions(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    # Insert default admin account
    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
                      ("admin", "admin123"))

    #  Insert Sample Data 
    cursor.execute("SELECT COUNT(*) FROM positions")
    if cursor.fetchone()[0] == 0:
        # Create positions
        cursor.execute("INSERT INTO positions (name) VALUES ('President')")
        cursor.execute("INSERT INTO positions (name) VALUES ('Vice President')")
        cursor.execute("INSERT INTO positions (name) VALUES ('Secretary')")

        # Get position IDs
        cursor.execute("SELECT id FROM positions WHERE name='President'")
        pres_id = cursor.fetchone()["id"]
        cursor.execute("SELECT id FROM positions WHERE name='Vice President'")
        vp_id = cursor.fetchone()["id"]
        cursor.execute("SELECT id FROM positions WHERE name='Secretary'")
        sec_id = cursor.fetchone()["id"]

        # Create sample candidates
        candidates_data = [
            ("Juan Dela Cruz", pres_id),
            ("Maria Santos", pres_id),
            ("Pedro Reyes", pres_id),
            ("Ana Gonzales", vp_id),
            ("Carlos Mendoza", vp_id),
            ("Sofia Reyes", sec_id),
            ("Miguel Torres", sec_id),
        ]
        cursor.executemany(
            "INSERT INTO candidates (full_name, position_id, votes) VALUES (?, ?, 0)",
            candidates_data
        )

    conn.commit()
    conn.close()
    print("Database initialized successfully!")