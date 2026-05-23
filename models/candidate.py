"""
Candidate model - Represents a candidate running for a position.
Handles all candidate-related database operations.
"""
import sqlite3


class Candidate:
    """Represents a single candidate in the election."""

    def __init__(self, id=None, full_name="", position_id=0, votes=0, image_path=None):
        self.id = id
        self.full_name = full_name
        self.position_id = position_id
        self.votes = votes
        self.image_path = image_path

    # Static Methods 

    @staticmethod
    def get_by_position(position_id):
        """
        Get all candidates for a specific position.
        Returns list of Candidate objects sorted alphabetically.
        """
        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, full_name, position_id, image_path, votes "
            "FROM candidates WHERE position_id=? ORDER BY full_name",
            (position_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            Candidate(row["id"], row["full_name"], row["position_id"],
                     row["votes"], row["image_path"])
            for row in rows
        ]

    @staticmethod
    def get_by_id(candidate_id):
        """Get a single candidate by ID. Returns Candidate or None."""
        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM candidates WHERE id=?", (candidate_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Candidate(row["id"], row["full_name"], row["position_id"],
                           row["votes"], row["image_path"])
        return None

    @staticmethod
    def get_all():
        """Get all candidates with their position names (for results)."""
        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.full_name, c.position_id, c.votes, c.image_path,
                   p.name as position_name
            FROM candidates c
            JOIN positions p ON c.position_id = p.id
            ORDER BY c.votes DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        candidates = []
        for row in rows:
            c = Candidate(row["id"], row["full_name"], row["position_id"],
                         row["votes"], row["image_path"])
            c.position_name = row["position_name"]
            candidates.append(c)
        return candidates

    # Instance Methods 

    def save(self):
        """Insert this candidate into the database."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO candidates (full_name, position_id, image_path) VALUES (?, ?, ?)",
            (self.full_name, self.position_id, self.image_path)
        )
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def update(self, new_name, new_image_path=None):
        """Update this candidate's name and optionally the image."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        if new_image_path:
            cursor.execute(
                "UPDATE candidates SET full_name=?, image_path=? WHERE id=?",
                (new_name, new_image_path, self.id)
            )
        else:
            cursor.execute(
                "UPDATE candidates SET full_name=? WHERE id=?",
                (new_name, self.id)
            )
        conn.commit()
        conn.close()
        self.full_name = new_name
        if new_image_path:
            self.image_path = new_image_path

    def delete(self):
        """Delete this candidate from the database."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM candidates WHERE id=?", (self.id,))
        conn.commit()
        conn.close()

    def increment_vote(self):
        """Add one vote to this candidate."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE id=?", (self.id,))
        conn.commit()
        conn.close()
        self.votes += 1

    def get_voters(self):
        """Get list of voter emails who voted for this candidate."""
        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT voter_email FROM votes WHERE candidate_id=?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["voter_email"] for row in rows]

    def to_dict(self):
        """Convert candidate to dictionary (useful for display)."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "position_id": self.position_id,
            "votes": self.votes,
            "image_path": self.image_path
        }