"""
Voter model - Represents a registered voter.
Handles voter verification and recording.
"""
import sqlite3


class Voter:
    """Represents a single voter."""

    def __init__(self, email="", has_voted=False):
        self.email = email
        self.has_voted = has_voted

    # Static Methods 
    @staticmethod
    def is_valid_email(email):
        """Check if email follows the school format."""
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@umindanao\.edu\.ph$"
        return bool(re.match(pattern, email))

    @staticmethod
    def has_already_voted(email):
        """Check if a voter has already cast their vote."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("SELECT has_voted FROM voters WHERE email=?", (email,))
        row = cursor.fetchone()
        conn.close()
        return row is not None and row[0] == 1

    @staticmethod
    def get_all():
        """Get all registered voters."""
        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT email, has_voted FROM voters")
        rows = cursor.fetchall()
        conn.close()
        return [Voter(row["email"], bool(row["has_voted"])) for row in rows]

    @staticmethod
    def reset_all():
        """Remove all voter records (for election reset)."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM voters")
        conn.commit()
        conn.close()

    # Instance Methods 

    def record(self):
        """Mark this voter as having voted."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO voters (email, has_voted) VALUES (?, 1)",
            (self.email,)
        )
        conn.commit()
        conn.close()
        self.has_voted = True