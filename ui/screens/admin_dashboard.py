"""
Admin dashboard screen - Contains tabbed interface for managing the election.
"""
import tkinter as tk
from tkinter import messagebox
from models.admin import Admin
from ui.styles import *
from ui.components.buttons import WarningButton, DangerButton


class AdminDashboard(tk.Frame):
    """Main admin dashboard with tabbed navigation."""

    def __init__(self, parent, username="Admin", on_logout=None):
        super().__init__(parent, bg=BG_MAIN)
        self.username = username
        self.on_logout = on_logout
        self.tab_buttons = {}
        self.current_tab = None

        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._build_ui()

    def _build_ui(self):
        """Build the dashboard UI."""
        # Top bar
        top = tk.Frame(self, bg=BG_DARK, height=50)
        top.pack(fill="x")
        top.pack_propagate(False)

        # Left side - Title
        tk.Label(top, text="Admin Dashboard", font=FONT_TITLE,
                bg=BG_DARK, fg="white").pack(side="left", padx=20)

        # Right side - Username + buttons
        right_frame = tk.Frame(top, bg=BG_DARK)
        right_frame.pack(side="right", padx=10)

        # Admin username display
        user_frame = tk.Frame(right_frame, bg=BG_DARK)
        user_frame.pack(side="left", padx=(0, 15))

        # User icon + username
        tk.Label(user_frame, text="👤", font=("Arial", 12),
                bg=BG_DARK, fg="white").pack(side="left", padx=(0, 5))
        tk.Label(user_frame, text=self.username, font=FONT_SMALL,
                bg=BG_DARK, fg=LIGHT_TEXT).pack(side="left")

        # Reset button
        WarningButton(right_frame, "Reset", self._reset_election,
                     width=8, font_size=9).pack(side="left", padx=5, pady=8)
        # Logout button
        DangerButton(right_frame, "Logout", self.on_logout,
                    width=8, font_size=9).pack(side="left", padx=5, pady=8)

        # Tab buttons
        tabs_frame = tk.Frame(self, bg=BG_WHITE, height=40)
        tabs_frame.pack(fill="x")
        tabs_frame.pack_propagate(False)

        for tab_id, tab_text in [
            ("manage", "Manage Candidates"),
            ("voters", "View Voters"),
            ("results", "View Results"),
            ("admins", "Manage Admins")
        ]:
            btn = tk.Button(tabs_frame, text=tab_text, font=FONT_SMALL,
                          bg=BG_WHITE, fg=DARK_TEXT, relief="flat",
                          cursor="hand2", padx=20,
                          command=lambda t=tab_id: self._switch_tab(t))
            btn.pack(side="left", pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=LIGHT_BLUE))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BG_WHITE))
            self.tab_buttons[tab_id] = btn

        # Content area
        self.content = tk.Frame(self, bg=BG_MAIN)
        self.content.pack(fill="both", expand=True)

        # Load default tab
        self._switch_tab("manage")

    def _switch_tab(self, tab_id):
        """Switch between admin tabs."""
        for tid, btn in self.tab_buttons.items():
            if tid == tab_id:
                btn.configure(bg=LIGHT_BLUE, fg=BLUE)
            else:
                btn.configure(bg=BG_WHITE, fg=DARK_TEXT)

        for widget in self.content.winfo_children():
            widget.destroy()

        if tab_id == "manage":
            from ui.admin_tabs.manage_candidates import ManageCandidatesTab
            self.current_tab = ManageCandidatesTab(self.content, self)
        elif tab_id == "voters":
            from ui.admin_tabs.view_voters import ViewVotersTab
            self.current_tab = ViewVotersTab(self.content)
        elif tab_id == "results":
            from ui.admin_tabs.view_results import ViewResultsTab
            self.current_tab = ViewResultsTab(self.content)
        elif tab_id == "admins":
            from ui.admin_tabs.manage_admins import ManageAdminsTab
            self.current_tab = ManageAdminsTab(self.content)

    def _reset_election(self):
        """Reset all election data."""
        if not messagebox.askyesno("Reset Election",
                                   "This will clear all votes and voter records.\n"
                                   "Candidates and positions will be kept.\n\n"
                                   "Are you sure?"):
            return
        Admin.reset_election()
        messagebox.showinfo("Reset Complete", "Election has been reset!")
        self._switch_tab("manage")