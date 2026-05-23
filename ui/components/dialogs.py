"""
Dialog components for add/edit operations.
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from ui.styles import *
from ui.components.buttons import SuccessButton, WarningButton, GrayButton
from ui.components.labels import BaseLabel, HeadingLabel


class CandidateDialog:
    """Base dialog for adding or editing a candidate."""

    def __init__(self, parent, title, candidate=None, on_save=None):
        self.parent = parent
        self.candidate = candidate
        self.on_save = on_save
        self.image_path_var = tk.StringVar()

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.configure(bg=BG_WHITE)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # CENTER THE DIALOG 
        self._center_dialog()

        self._build_ui()
        if candidate:
            self._prefill()

    def _center_dialog(self):
        """Center the dialog over its parent window."""
        self.dialog.update_idletasks()

        # Get parent dimensions
        parent_w = self.parent.winfo_width()
        parent_h = self.parent.winfo_height()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()

        # Get dialog dimensions
        dialog_w = 400
        dialog_h = 350

        # Calculate center position
        x = parent_x + (parent_w - dialog_w) // 2
        y = parent_y + (parent_h - dialog_h) // 2

        self.dialog.geometry(f"{dialog_w}x{dialog_h}+{x}+{y}")

    def _build_ui(self):
        """Build the dialog UI."""
        HeadingLabel(self.dialog, self.dialog.title()).pack(pady=15)

        # Name field
        BaseLabel(self.dialog, "Full Name:", font=FONT_SMALL).pack(anchor="w", padx=30, pady=(10, 5))
        self.name_entry = tk.Entry(self.dialog, font=FONT_NORMAL, width=30)
        self.name_entry.pack(padx=30, pady=(0, 10))
        self.name_entry.focus()

        # Image field
        BaseLabel(self.dialog, "Image (optional):", font=FONT_SMALL).pack(anchor="w", padx=30, pady=(10, 5))
        self.browse_btn = GrayButton(self.dialog, "Browse Image",
                                      self._browse_image, width=15, font_size=9)
        self.browse_btn.pack(pady=5)

        # Save button
        SuccessButton(self.dialog, "Save", self._save, width=10).pack(pady=20)

    def _prefill(self):
        """Pre-fill fields when editing an existing candidate."""
        self.name_entry.insert(0, self.candidate.full_name)

    def _browse_image(self):
        """Open file dialog to select an image."""
        file = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if file:
            self.image_path_var.set(file)
            self.browse_btn.configure(text="✓ Image Selected", bg=GREEN)

    def _save_image(self, img_path):
        """Copy image to assets/candidates/ folder."""
        if not img_path or not os.path.exists(img_path):
            return None
        try:
            os.makedirs("assets/candidates", exist_ok=True)
            filename = os.path.basename(img_path)
            dest = os.path.join("assets", "candidates", filename)
            if img_path != dest:
                shutil.copy(img_path, dest)
            return dest
        except Exception:
            return None

    def _save(self):
        """Validate and save."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name is required", parent=self.dialog)
            return

        img_path = None
        if self.image_path_var.get():
            img_path = self._save_image(self.image_path_var.get())

        if self.on_save:
            self.on_save(name, img_path)

        self.dialog.destroy()


class PositionDialog:
    """Simple dialog for adding a position name."""

    def __init__(self, parent, on_save=None):
        self.on_save = on_save
        name = tk.simpledialog.askstring("Add Position", "Enter position name:", parent=parent)
        if name and on_save:
            on_save(name)


class EditPositionDialog:
    """Dialog for editing a position name."""

    def __init__(self, parent, current_name, on_save=None):
        self.on_save = on_save
        new_name = tk.simpledialog.askstring("Edit Position",
                                             "Enter new position name:",
                                             initialvalue=current_name,
                                             parent=parent)
        if new_name and new_name != current_name and on_save:
            on_save(new_name)