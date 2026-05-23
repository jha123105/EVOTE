"""
Position model - Represents an election position (President, VP, etc.).
Handles all position-related database operations.
"""
import sqlite3


class Position:
    """Represents a single election position."""

    def __init__(self, id=None, name=""):
        self.id = id
        self.name = name

    # Static Methods 

    @staticmethod
    def get_all():
        """Get all positions. Returns list of Position objects."""
        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM positions")
        rows = cursor.fetchall()
        conn.close()
        return [Position(row["id"], row["name"]) for row in rows]

    @staticmethod
    def get_by_id(position_id):
        """Get a single position by ID. Returns Position or None."""
        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM positions WHERE id=?", (position_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Position(row["id"], row["name"])
        return None

    # Instance Methods 

    def save(self):
        """Insert this position into the database."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO positions (name) VALUES (?)", (self.name,))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def update(self, new_name):
        """Update this position's name."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE positions SET name=? WHERE id=?", (new_name, self.id))
        conn.commit()
        conn.close()
        self.name = new_name

    def delete(self):
        """Delete this position and all related candidates/votes."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM votes WHERE position_id=?", (self.id,))
        cursor.execute("DELETE FROM candidates WHERE position_id=?", (self.id,))
        cursor.execute("DELETE FROM positions WHERE id=?", (self.id,))
        conn.commit()
        conn.close()

    def get_results(self):
        """Get election results for this position, sorted by votes."""
        from models.candidate import Candidate
        candidates = Candidate.get_by_position(self.id)
        candidates.sort(key=lambda c: c.votes, reverse=True)
        return candidates