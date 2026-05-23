"""
Manage Admins tab - Change password and manage admin accounts.
"""
import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui.styles import *
from ui.components.buttons import SuccessButton, DangerButton, PrimaryButton
from ui.components.labels import HeadingLabel, BaseLabel, SubtitleLabel


class ManageAdminsTab(tk.Frame):
    """Tab for managing admin accounts."""

    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        """Build the manage admins UI."""
        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Left Panel - Change Password
        left = tk.Frame(main, bg=BG_WHITE, relief="solid", borderwidth=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        HeadingLabel(left, "Change Password").pack(pady=15)

        form = tk.Frame(left, bg=BG_WHITE)
        form.pack(padx=30, pady=10, fill="x")

        # Current password
        BaseLabel(form, "Current Password:", font=FONT_SMALL).pack(anchor="w", pady=(10, 5))
        self.current_pw = tk.Entry(form, font=FONT_NORMAL, show="•", width=30)
        self.current_pw.pack(fill="x", pady=(0, 10))

        # New password
        BaseLabel(form, "New Password:", font=FONT_SMALL).pack(anchor="w", pady=(10, 5))
        self.new_pw = tk.Entry(form, font=FONT_NORMAL, show="•", width=30)
        self.new_pw.pack(fill="x", pady=(0, 10))

        # Confirm new password
        BaseLabel(form, "Confirm New Password:", font=FONT_SMALL).pack(anchor="w", pady=(10, 5))
        self.confirm_pw = tk.Entry(form, font=FONT_NORMAL, show="•", width=30)
        self.confirm_pw.pack(fill="x", pady=(0, 15))

        SuccessButton(form, "Update Password", self._change_password, width=18).pack(pady=10)

        # Right Panel - Add Admin Account 
        right = tk.Frame(main, bg=BG_WHITE, relief="solid", borderwidth=1)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        HeadingLabel(right, "Add New Admin").pack(pady=15)

        form2 = tk.Frame(right, bg=BG_WHITE)
        form2.pack(padx=30, pady=10, fill="x")

        # Username
        BaseLabel(form2, "Username:", font=FONT_SMALL).pack(anchor="w", pady=(10, 5))
        self.new_username = tk.Entry(form2, font=FONT_NORMAL, width=30)
        self.new_username.pack(fill="x", pady=(0, 10))

        # Password
        BaseLabel(form2, "Password:", font=FONT_SMALL).pack(anchor="w", pady=(10, 5))
        self.new_admin_pw = tk.Entry(form2, font=FONT_NORMAL, show="•", width=30)
        self.new_admin_pw.pack(fill="x", pady=(0, 15))

        PrimaryButton(form2, "Create Admin", self._add_admin, width=18).pack(pady=10)

        # Existing Admins List 
        list_frame = tk.Frame(right, bg=BG_WHITE)
        list_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        SubtitleLabel(list_frame, "Existing Admin Accounts:").pack(anchor="w", pady=(10, 5))
        self.admin_list = tk.Frame(list_frame, bg=BG_WHITE)
        self.admin_list.pack(fill="both", expand=True)
        self._load_admin_list()

    def _change_password(self):
        """Change the current admin's password."""
        current = self.current_pw.get().strip()
        new = self.new_pw.get().strip()
        confirm = self.confirm_pw.get().strip()

        if not current or not new or not confirm:
            messagebox.showerror("Error", "All fields are required.")
            return

        if new != confirm:
            messagebox.showerror("Error", "New passwords do not match.")
            return

        if len(new) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters.")
            return

        # Verify current password
        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE password=?", (current,))
        if not cursor.fetchone():
            conn.close()
            messagebox.showerror("Error", "Current password is incorrect.")
            return

        # Update password (update all admins with this password, or just the first)
        cursor.execute("UPDATE admin SET password=? WHERE password=?", (new, current))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", " Password updated successfully!")
        self.current_pw.delete(0, tk.END)
        self.new_pw.delete(0, tk.END)
        self.confirm_pw.delete(0, tk.END)

    def _add_admin(self):
        """Add a new admin account."""
        username = self.new_username.get().strip()
        password = self.new_admin_pw.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters.")
            return

        conn = sqlite3.connect("evote.db")
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM admin WHERE username=?", (username,))
        if cursor.fetchone():
            conn.close()
            messagebox.showerror("Error", f"Username '{username}' already exists.")
            return

        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
                      (username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f" Admin '{username}' created!")
        self.new_username.delete(0, tk.END)
        self.new_admin_pw.delete(0, tk.END)
        self._load_admin_list()

    def _load_admin_list(self):
        """Load and display all admin accounts."""
        for widget in self.admin_list.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("evote.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM admin")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            SubtitleLabel(self.admin_list, "No admin accounts found.").pack()
            return

        for i, row in enumerate(rows):
            bg = LIGHT_GRAY if i % 2 == 0 else BG_WHITE
            item_frame = tk.Frame(self.admin_list, bg=bg, height=30)
            item_frame.pack(fill="x")
            item_frame.pack_propagate(False)

            tk.Label(item_frame, text=f"👤 {row['username']}",
                    font=FONT_SMALL, bg=bg, fg=DARK_TEXT).pack(
                side="left", padx=15, pady=5)

            # Don't allow deleting the last admin
            if len(rows) > 1:
                DangerButton(item_frame, "Delete",
                           lambda u=row['username']: self._delete_admin(u),
                           width=8, font_size=8).pack(side="right", padx=10, pady=3)

    def _delete_admin(self, username):
        """Delete an admin account."""
        if messagebox.askyesno("Confirm Delete",
                               f"Delete admin '{username}'?\n\nThis cannot be undone."):
            conn = sqlite3.connect("evote.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM admin WHERE username=?", (username,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f" Admin '{username}' deleted!")
            self._load_admin_list()