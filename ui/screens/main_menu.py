"""
Main menu screen - The landing page with Start Voting and Admin Panel buttons.
"""
import tkinter as tk
from PIL import Image, ImageTk
import os
from ui.styles import *
from ui.components.buttons import PrimaryButton, DarkButton
from ui.components.labels import LargeTitleLabel, SubtitleLabel, BaseLabel


class MainMenu(tk.Frame):
    """Main menu screen displayed on application launch."""

    def __init__(self, parent, on_start_voting, on_admin_panel):
        super().__init__(parent, bg=BG_MAIN)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._build_ui(on_start_voting, on_admin_panel)

    def _build_ui(self, on_start_voting, on_admin_panel):
        """Build the main menu UI."""
        center = tk.Frame(self, bg=BG_MAIN)
        center.place(relx=0.5, rely=0.45, anchor="center")

        # Logo
        if os.path.exists("assets/logo.png"):
            try:
                img = Image.open("assets/logo.png")
                img = img.resize((100, 100), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(center, image=self.logo_img, bg=BG_MAIN).pack(pady=(0, 20))
            except Exception:
                pass

        # Title
        LargeTitleLabel(center, "E-VOTE").pack()
        SubtitleLabel(center, "School Election System").pack(pady=(5, 30))

        # Action buttons
        PrimaryButton(center, "Start Voting", on_start_voting,
                     width=20, font_size=13).pack(pady=5)
        DarkButton(center, "Admin Panel", on_admin_panel,
                   width=20, font_size=13).pack(pady=5)

        # Footer
        BaseLabel(self, "© 2024 E-Vote System", font=FONT_TINY, fg=GRAY).place(
            relx=0.5, rely=0.97, anchor="s")