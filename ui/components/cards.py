"""
Reusable card components for displaying candidates.
"""
import tkinter as tk
import os
from PIL import Image, ImageTk
from ui.styles import *
from ui.components.buttons import PrimaryButton, SuccessButton, WarningButton, DangerButton
from ui.components.labels import BaseLabel, SubtitleLabel


class CandidateCard(tk.Frame):
    """
    Card component for displaying a candidate in the voter panel.
    Shows image, name, position, and vote/selected button.
    """

    def __init__(self, parent, candidate, position_name, is_selected=False,
                 on_vote=None, on_deselect=None):
        super().__init__(parent, bg=BG_WHITE, width=CARD_WIDTH, height=CARD_HEIGHT,
                        relief="solid", borderwidth=1)
        self.pack_propagate(False)

        # Image frame
        img_frame = tk.Frame(self, bg=LIGHT_BLUE, height=150)
        img_frame.pack(fill="x")
        img_frame.pack_propagate(False)
        self._load_image(img_frame, candidate, CARD_WIDTH, 150)

        # Info frame
        info = tk.Frame(self, bg=BG_WHITE)
        info.pack(fill="both", expand=True, padx=10, pady=8)

        BaseLabel(info, candidate.full_name, font=FONT_SMALL).pack()
        SubtitleLabel(info, position_name).pack(pady=(2, 8))

        # Vote button
        if is_selected:
            SuccessButton(info, "✓ Selected", on_deselect, width=10, font_size=9).pack()
        else:
            PrimaryButton(info, "Vote", on_vote, width=10, font_size=9).pack()

    def _load_image(self, parent, candidate, width, height):
        """Load and display candidate image or fallback initial."""
        for widget in parent.winfo_children():
            widget.destroy()

        img_path = getattr(candidate, 'image_path', None)
        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                img = img.resize((width, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(parent, image=photo, bg=LIGHT_BLUE, borderwidth=0, highlightthickness=0)
                lbl.image = photo
                lbl.place(x=0, y=0, relwidth=1, relheight=1)
                return
            except Exception:
                pass

        # Fallback: show first letter
        initial = candidate.full_name[0].upper() if candidate.full_name else "?"
        tk.Label(parent, text=initial, font=("Arial", 40, "bold"),
                bg=LIGHT_BLUE, fg=BLUE).place(relx=0.5, rely=0.5, anchor="center")


class AdminCandidateCard(tk.Frame):
    """
    Card component for displaying a candidate in the admin panel.
    Shows image, name, votes, and edit/delete buttons.
    """

    def __init__(self, parent, candidate, position_name,
                 on_edit=None, on_delete=None):
        super().__init__(parent, bg=BG_WHITE, width=CARD_WIDTH, height=CARD_HEIGHT,
                        relief="solid", borderwidth=1)
        self.pack_propagate(False)

        # Image frame
        img_frame = tk.Frame(self, bg=LIGHT_BLUE, height=150)
        img_frame.pack(fill="x")
        img_frame.pack_propagate(False)
        self._load_image(img_frame, candidate, CARD_WIDTH, 150)

        # Info frame
        info = tk.Frame(self, bg=BG_WHITE)
        info.pack(fill="both", expand=True, padx=10, pady=8)

        BaseLabel(info, candidate.full_name, font=FONT_SMALL).pack()
        SubtitleLabel(info, f"Votes: {candidate.votes}").pack(pady=(2, 8))

        # Action buttons
        btns = tk.Frame(info, bg=BG_WHITE)
        btns.pack()
        WarningButton(btns, "Edit", on_edit, width=6, font_size=8).pack(side="left", padx=2)
        DangerButton(btns, "Del", on_delete, width=6, font_size=8).pack(side="left", padx=2)

    def _load_image(self, parent, candidate, width, height):
        """Load and display candidate image or fallback initial."""
        for widget in parent.winfo_children():
            widget.destroy()

        img_path = getattr(candidate, 'image_path', None)
        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                img = img.resize((width, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(parent, image=photo, bg=LIGHT_BLUE, borderwidth=0, highlightthickness=0)
                lbl.image = photo
                lbl.place(x=0, y=0, relwidth=1, relheight=1)
                return
            except Exception:
                pass

        # Fallback: show first letter
        initial = candidate.full_name[0].upper() if candidate.full_name else "?"
        tk.Label(parent, text=initial, font=("Arial", 40, "bold"),
                bg=LIGHT_BLUE, fg=BLUE).place(relx=0.5, rely=0.5, anchor="center")


class AddCandidateCard(tk.Frame):
    """Special card with '+' button to add a new candidate."""

    def __init__(self, parent, on_add=None):
        super().__init__(parent, bg=BG_WHITE, width=CARD_WIDTH, height=CARD_HEIGHT,
                        relief="solid", borderwidth=1)
        self.pack_propagate(False)

        img_frame = tk.Frame(self, bg=LIGHT_BLUE, height=150)
        img_frame.pack(fill="x")
        img_frame.pack_propagate(False)
        tk.Label(img_frame, text="+", font=("Arial", 48, "bold"),
                bg=LIGHT_BLUE, fg=BLUE).pack(expand=True)

        info = tk.Frame(self, bg=BG_WHITE)
        info.pack(fill="both", expand=True)
        tk.Label(info, text="Add Candidate", font=FONT_SMALL,
                bg=BG_WHITE, fg=DARK_TEXT).pack(pady=15)
        SuccessButton(info, "Add", on_add, width=10, font_size=9).pack()