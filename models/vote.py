"""
Vote model - Records individual votes cast.
"""
import sqlite3


class Vote:
    """Represents a single vote cast by a voter."""

    def __init__(self, voter_email="", candidate_id=0, position_id=0):
        self.voter_email = voter_email
        self.candidate_id = candidate_id
        self.position_id = position_id

    # Instance Methods 

    def record(self):
        """Record this vote in the database."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO votes (voter_email, candidate_id, position_id) VALUES (?, ?, ?)",
            (self.voter_email, self.candidate_id, self.position_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_voters_by_candidate(candidate_id):
        """Get all voter emails who voted for a specific candidate."""
        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT voter_email FROM votes WHERE candidate_id=?",
            (candidate_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [row["voter_email"] for row in rows]

    @staticmethod
    def clear_all():
        """Remove all votes (for election reset)."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM votes")
        conn.commit()
        conn.close()