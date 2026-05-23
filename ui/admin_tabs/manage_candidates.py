"""
Manage Candidates tab - Add, edit, delete positions and candidates.
"""
import tkinter as tk
from tkinter import messagebox
from models.position import Position
from models.candidate import Candidate
from ui.styles import *
from ui.components.buttons import SuccessButton, WarningButton, DangerButton, GrayButton
from ui.components.labels import HeadingLabel, BaseLabel
from ui.components.cards import AdminCandidateCard, AddCandidateCard
from ui.components.dialogs import CandidateDialog, PositionDialog, EditPositionDialog


class ManageCandidatesTab(tk.Frame):
    """Tab for managing positions and candidates."""

    def __init__(self, parent, dashboard):
        super().__init__(parent, bg=BG_MAIN)
        self.dashboard = dashboard
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        """Build the manage candidates UI."""
        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Left sidebar - Positions
        left = tk.Frame(main, bg=BG_WHITE, width=200, relief="solid", borderwidth=1)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        HeadingLabel(left, "Positions").pack(pady=15)

        pos_list = tk.Frame(left, bg=BG_WHITE)
        pos_list.pack(fill="both", expand=True, padx=10)

        self.selected_position_id = None
        self.position_buttons = {}

        positions = Position.get_all()
        for pos in positions:
            btn = tk.Button(pos_list, text=pos.name, font=FONT_SMALL,
                          bg=BG_WHITE, fg=DARK_TEXT, relief="flat",
                          cursor="hand2", anchor="w", width=18,
                          command=lambda p=pos: self._select_position(p.id))
            btn.pack(pady=2)
            self.position_buttons[pos.id] = btn

        # Position action buttons
        actions = tk.Frame(left, bg="#f0f0f0", height=50)
        actions.pack(side="bottom", fill="x")
        actions.pack_propagate(False)
        btns = tk.Frame(actions, bg="#f0f0f0")
        btns.pack(expand=True, pady=5)
        SuccessButton(btns, "Add", self._add_position, width=5, font_size=9).pack(
            side="left", padx=3)
        WarningButton(btns, "Edit", self._edit_position, width=5, font_size=9).pack(
            side="left", padx=3)
        DangerButton(btns, "Delete", self._delete_position, width=5, font_size=9).pack(
            side="left", padx=3)

        # Right panel - Candidates
        self.right = tk.Frame(main, bg=BG_WHITE, relief="solid", borderwidth=1)
        self.right.pack(side="left", fill="both", expand=True, padx=(15, 0))

        if positions:
            self._select_position(positions[0].id)

    def _select_position(self, position_id):
        """Select a position and load its candidates."""
        for pid, btn in self.position_buttons.items():
            btn.configure(bg=LIGHT_BLUE if pid == position_id else BG_WHITE,
                         fg=BLUE if pid == position_id else DARK_TEXT)
        self.selected_position_id = position_id
        self._load_candidates()

    def _load_candidates(self):
        """Load candidates for the selected position."""
        for widget in self.right.winfo_children():
            widget.destroy()

        # Header
        header = tk.Frame(self.right, bg=BG_WHITE, height=40)
        header.pack(fill="x", padx=15, pady=10)
        HeadingLabel(header, "Candidates").pack(side="left")
        GrayButton(header, "Refresh", self._load_candidates, width=8, font_size=9).pack(
            side="right")

        # Candidate grid
        grid = tk.Frame(self.right, bg=BG_WHITE)
        grid.pack(fill="both", expand=True, padx=15, pady=10)

        candidates = Candidate.get_by_position(self.selected_position_id)
        row, col = 0, 0

        # Add candidate card
        AddCandidateCard(grid, self._add_candidate).grid(
            row=row, column=col, padx=10, pady=10)
        col += 1

        # Candidate cards
        pos_name = ""
        for p in Position.get_all():
            if p.id == self.selected_position_id:
                pos_name = p.name
                break

        for cand in candidates:
            AdminCandidateCard(
                grid, cand, pos_name,
                on_edit=lambda c=cand: self._edit_candidate(c),
                on_delete=lambda c=cand: self._delete_candidate(c)
            ).grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col >= 4:
                col = 0
                row += 1

    def _add_position(self):
        """Add a new position."""
        PositionDialog(self, on_save=lambda name: self._save_position(name))

    def _save_position(self, name):
        """Save a new position to database."""
        pos = Position(name=name)
        pos.save()
        messagebox.showinfo("Success", " Position added!")
        # Refresh UI
        self.destroy()
        ManageCandidatesTab(self.master, self.dashboard)

    def _edit_position(self):
        """Edit the selected position name."""
        if not self.selected_position_id:
            messagebox.showinfo("Info", "Please select a position first.")
            return
        current = Position.get_by_id(self.selected_position_id)
        if current:
            EditPositionDialog(self, current.name,
                             on_save=lambda n: self._update_position(n))

    def _update_position(self, new_name):
        """Update position name."""
        pos = Position.get_by_id(self.selected_position_id)
        if pos:
            pos.update(new_name)
            messagebox.showinfo("Success", " Position updated!")
            self.destroy()
            ManageCandidatesTab(self.master, self.dashboard)

    def _delete_position(self):
        """Delete the selected position."""
        if not self.selected_position_id:
            messagebox.showinfo("Info", "Please select a position first.")
            return
        pos = Position.get_by_id(self.selected_position_id)
        if pos and messagebox.askyesno("Delete Position",
                                        f"Delete '{pos.name}' and all its candidates?"):
            pos.delete()
            messagebox.showinfo("Success", f" Position deleted!")
            self.destroy()
            ManageCandidatesTab(self.master, self.dashboard)

    def _add_candidate(self):
        """Open dialog to add a new candidate."""
        CandidateDialog(self, "Add Candidate",
                       on_save=lambda n, i: self._save_candidate(n, i))

    def _save_candidate(self, name, img_path):
        """Save new candidate."""
        cand = Candidate(full_name=name, position_id=self.selected_position_id,
                        image_path=img_path)
        cand.save()
        self._load_candidates()
        messagebox.showinfo("Success", " Candidate added!")

    def _edit_candidate(self, candidate):
        """Open dialog to edit an existing candidate."""
        CandidateDialog(self, "Edit Candidate", candidate,
                       on_save=lambda n, i: self._update_candidate(candidate.id, n, i))

    def _update_candidate(self, cand_id, new_name, img_path):
        """Update candidate info."""
        cand = Candidate.get_by_id(cand_id)
        if cand:
            cand.update(new_name, img_path)
            self._load_candidates()
            messagebox.showinfo("Success", " Candidate updated!")

    def _delete_candidate(self, candidate):
        """Delete a candidate."""
        if messagebox.askyesno("Confirm", "Delete this candidate?"):
            candidate.delete()
            self._load_candidates()