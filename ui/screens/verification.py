"""
Email verification screen - Validates school email before allowing voting.
"""
import tkinter as tk
from ui.styles import *
from ui.components.buttons import SuccessButton, TextButton
from ui.components.labels import BaseLabel, SubtitleLabel


class VerificationScreen(tk.Frame):
    """Screen where voter enters their school email for verification."""

    def __init__(self, parent, on_verify, on_back):
        super().__init__(parent, bg=BG_MAIN)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._build_ui(on_verify, on_back)

    def _build_ui(self, on_verify, on_back):
        """Build the verification UI."""
        # Back button
        TextButton(self, "← Back", on_back).place(x=20, y=20)

        # Card
        card = tk.Frame(self, bg=BG_WHITE, relief="solid", borderwidth=1,
                       width=400, height=300)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Header
        header = tk.Frame(card, bg=BLUE, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Email Verification", font=FONT_TITLE,
                bg=BLUE, fg="white").pack(expand=True)

        # Content
        content = tk.Frame(card, bg=BG_WHITE)
        content.pack(fill="both", expand=True, padx=30, pady=25)

        BaseLabel(content, "Enter your school email:", font=FONT_NORMAL).pack(pady=(0, 10))

        entry_frame = tk.Frame(content, bg=BG_WHITE, relief="solid", borderwidth=1)
        entry_frame.pack(fill="x", pady=(0, 15))
        self.email_entry = tk.Entry(entry_frame, font=FONT_NORMAL, relief="flat", borderwidth=0)
        self.email_entry.pack(padx=10, pady=8, fill="x")

        SuccessButton(content, "Verify",
                     lambda: on_verify(self.email_entry.get()),
                     width=12).pack(pady=(0, 10))

        SubtitleLabel(content, "e.g., student@umindanao.edu.ph").pack()

    def get_email(self):
        """Return the entered email."""
        return self.email_entry.get().strip()