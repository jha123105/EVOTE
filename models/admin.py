"""
Admin model - Handles admin authentication.
"""
import sqlite3


class Admin:
    """Represents an admin user."""

    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

    # Static Methods 

    @staticmethod
    def validate(username, password):
        """Check if admin credentials are correct."""
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username, password)
        )
        row = cursor.fetchone()
        conn.close()
        return row is not None

    @staticmethod
    def reset_election():
        """
        Reset all election data:
        - Clear all votes
        - Remove all voter records
        - Reset candidate vote counts to 0
        Keeps positions and candidates intact.
        """
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM votes")
        cursor.execute("DELETE FROM voters")
        cursor.execute("UPDATE candidates SET votes = 0")
        conn.commit()
        conn.close()
        print("Election data has been reset!")