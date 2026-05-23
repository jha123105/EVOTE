"""
Main App class - Manages the application window and screen switching.
Uses composition to switch between screens.
"""
import tkinter as tk
from tkinter import messagebox
from models.voter import Voter
from models.admin import Admin
from ui.styles import *
from ui.screens.main_menu import MainMenu
from ui.screens.verification import VerificationScreen
from ui.screens.voter_panel import VoterPanel
from ui.screens.admin_login import AdminLogin
from ui.screens.admin_dashboard import AdminDashboard


class App:
    """
    Main application class.
    Manages the root window and switches between screens.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("E-Vote System")
        self.root.configure(bg=BG_MAIN)

        # Window setup
        try:
            self.root.attributes("-zoomed", True)
        except Exception:
            self.root.geometry(WINDOW_SIZE)

        # Set app icon
        try:
            self.root.iconphoto(False, tk.PhotoImage(file="assets/logo.png"))
        except Exception:
            pass

        # Container for screens
        self.container = tk.Frame(self.root, bg=BG_MAIN)
        self.container.pack(fill="both", expand=True)

        # Show main menu
        self.show_main_menu()

    def clear_container(self):
        """Remove all widgets from the container."""
        for widget in self.container.winfo_children():
            widget.destroy()

    # Screen Navigation 

    def show_main_menu(self):
        """Show the main menu screen."""
        self.clear_container()
        MainMenu(self.container,
                on_start_voting=self.show_verification,
                on_admin_panel=self.show_admin_login)

    def show_verification(self):
        """Show the email verification screen."""
        self.clear_container()
        VerificationScreen(self.container,
                          on_verify=self.verify_email,
                          on_back=self.show_main_menu)

    def verify_email(self, email):
        """Verify voter email and show voting panel if valid."""
        email = email.strip().lower()

        if not email:
            messagebox.showerror("Error", "Email field cannot be empty.")
            return

        if not Voter.is_valid_email(email):
            messagebox.showerror("Error",
                               "Invalid school email. Use your @umindanao.edu.ph email.")
            return

        if Voter.has_already_voted(email):
            messagebox.showerror("Error", "This email has already voted.")
            return

        self.show_voter_panel(email)

    def show_voter_panel(self, email):
        """Show the voting panel for a verified voter."""
        self.clear_container()
        VoterPanel(self.container, email,
                  on_submit_complete=self.show_main_menu)

    def show_admin_login(self):
        """Show the admin login screen."""
        self.clear_container()
        AdminLogin(self.container,
                  on_login=self.admin_login,
                  on_back=self.show_main_menu)

    def admin_login(self, username, password):
        """Authenticate admin and show dashboard."""
        if Admin.validate(username, password):
            self.show_admin_dashboard(username)   # Pass username
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def show_admin_dashboard(self, username="Admin"):
        """Show the admin dashboard."""
        self.clear_container()
        AdminDashboard(self.container,
                      username=username,           # Pass username
                      on_logout=self.show_main_menu)

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()