"""
Admin login screen - Authentication for admin panel access.
"""
import tkinter as tk
from ui.styles import *
from ui.components.buttons import DarkButton, TextButton
from ui.components.labels import BaseLabel


class AdminLogin(tk.Frame):
    """Admin login screen."""

    def __init__(self, parent, on_login, on_back):
        super().__init__(parent, bg=BG_MAIN)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._build_ui(on_login, on_back)

    def _build_ui(self, on_login, on_back):
        """Build the login UI."""
        TextButton(self, "← Back", on_back).place(x=20, y=20)

        # Card
        card = tk.Frame(self, bg=BG_WHITE, relief="solid", borderwidth=1,
                       width=350, height=300)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Header
        header = tk.Frame(card, bg=BG_DARK, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Admin Login", font=FONT_TITLE,
                bg=BG_DARK, fg="white").pack(expand=True)

        # Content
        content = tk.Frame(card, bg=BG_WHITE)
        content.pack(fill="both", expand=True, padx=30, pady=25)

        BaseLabel(content, "Username:", font=FONT_SMALL).pack(anchor="w", pady=(0, 5))
        frame1 = tk.Frame(content, bg=BG_WHITE, relief="solid", borderwidth=1)
        frame1.pack(fill="x", pady=(0, 15))
        self.username_entry = tk.Entry(frame1, font=FONT_NORMAL, relief="flat", borderwidth=0)
        self.username_entry.pack(padx=10, pady=8, fill="x")

        BaseLabel(content, "Password:", font=FONT_SMALL).pack(anchor="w", pady=(0, 5))
        frame2 = tk.Frame(content, bg=BG_WHITE, relief="solid", borderwidth=1)
        frame2.pack(fill="x", pady=(0, 20))
        self.password_entry = tk.Entry(frame2, font=FONT_NORMAL, relief="flat",
                                       borderwidth=0, show="•")
        self.password_entry.pack(padx=10, pady=8, fill="x")

        DarkButton(content, "Sign In",
                  lambda: on_login(self.username_entry.get(), self.password_entry.get()),
                  width=12).pack()