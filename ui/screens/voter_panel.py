"""
Voter panel screen - Where voters select candidates and submit votes.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.position import Position
from models.candidate import Candidate
from ui.styles import *
from ui.components.buttons import SuccessButton, TextButton
from ui.components.labels import BaseLabel, HeadingLabel
from ui.components.cards import CandidateCard


class VoterPanel(tk.Frame):
    """Main voting panel where voters select candidates by position."""

    def __init__(self, parent, voter_email, on_submit_complete):
        super().__init__(parent, bg=BG_MAIN)
        self.voter_email = voter_email
        self.on_submit_complete = on_submit_complete
        self.selected = {}  # {position_id: candidate_id}
        self.candidate_cards = []  # Keep references to prevent garbage collection

        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._build_ui()

    def _build_ui(self):
        """Build the voting panel UI."""
        # Top bar - FIXED: Added back/logout button
        top = tk.Frame(self, bg=BG_WHITE, height=50, relief="solid", borderwidth=1)
        top.pack(fill="x")
        top.pack_propagate(False)
        TextButton(top, "← Logout", self._confirm_logout).pack(side="left", padx=10, pady=10)
        tk.Label(top, text="E-VOTE", font=FONT_TITLE, bg=BG_WHITE, fg=BLUE).pack(
            side="left", padx=20)
        tk.Label(top, text=f"👤 {self.voter_email}", font=FONT_SMALL,
                bg=BG_WHITE, fg=LIGHT_TEXT).pack(side="right", padx=20)

        # Main content
        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Left sidebar - Positions
        left = tk.Frame(main, bg=BG_WHITE, width=200, relief="solid", borderwidth=1)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        HeadingLabel(left, "Positions").pack(pady=15)

        self.positions = Position.get_all()
        for pos in self.positions:
            btn = tk.Button(left, text=pos.name, font=FONT_SMALL,
                          bg=BG_WHITE, fg=DARK_TEXT, relief="flat",
                          cursor="hand2", anchor="w", width=18,
                          command=lambda p=pos.id: self._load_candidates(p))
            btn.pack(pady=2, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=LIGHT_BLUE))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BG_WHITE))

        # Right panel - Candidates
        right = tk.Frame(main, bg=BG_WHITE, relief="solid", borderwidth=1)
        right.pack(side="left", fill="both", expand=True, padx=(15, 0))

        HeadingLabel(right, "Candidates").pack(pady=15)

        # Scrollable candidate grid
        canvas = tk.Canvas(right, bg=BG_WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
        self.candidate_grid = tk.Frame(canvas, bg=BG_WHITE)

        self.candidate_grid.bind("<Configure>",
                                 lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.candidate_grid, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom bar - Selected and Submit
        bottom = tk.Frame(self, bg=BG_WHITE, height=60, relief="solid", borderwidth=1)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)

        tk.Label(bottom, text="Selected:", font=FONT_SMALL,
                bg=BG_WHITE, fg=DARK_TEXT).pack(side="left", padx=20)
        self.selected_frame = tk.Frame(bottom, bg=BG_WHITE)
        self.selected_frame.pack(side="left", padx=10)

        SuccessButton(bottom, "Submit Votes", self._submit_votes, width=15).pack(
            side="right", padx=20)

        # Load first position by default
        if self.positions:
            self._load_candidates(self.positions[0].id)

    def _confirm_logout(self):
        """Confirm before logging out (abandoning votes)."""
        if self.selected:
            if not messagebox.askyesno("Logout",
                                       "You have unsubmitted selections.\n"
                                       "Logging out will lose your votes.\n\n"
                                       "Are you sure?"):
                return
        self.on_submit_complete()

    def _load_candidates(self, position_id):
        """Load and display candidates for the selected position."""
        for widget in self.candidate_grid.winfo_children():
            widget.destroy()

        candidates = Candidate.get_by_position(position_id)
        pos_name = ""
        for p in self.positions:
            if p.id == position_id:
                pos_name = p.name
                break

        row, col = 0, 0
        for cand in candidates:
            is_selected = position_id in self.selected and self.selected[position_id] == cand.id

            card = CandidateCard(
                self.candidate_grid, cand, pos_name, is_selected,
                on_vote=lambda cid=cand.id, pid=position_id: self._select(pid, cid),
                on_deselect=lambda pid=position_id: self._deselect(pid)
            )
            card.grid(row=row, column=col, padx=10, pady=10)
            self.candidate_cards.append(card)

            col += 1
            if col >= 4:
                col = 0
                row += 1

        self.current_position = position_id

    def _select(self, position_id, candidate_id):
        """Select a candidate for a position."""
        self.selected[position_id] = candidate_id
        self._update_selected_bar()
        self._load_candidates(position_id)

    def _deselect(self, position_id):
        """Deselect the candidate for a position."""
        if position_id in self.selected:
            del self.selected[position_id]
        self._update_selected_bar()
        self._load_candidates(position_id)

    def _update_selected_bar(self):
        """Update the bottom bar showing selected candidates."""
        for widget in self.selected_frame.winfo_children():
            widget.destroy()

        for pos_id, cand_id in self.selected.items():
            candidate = Candidate.get_by_id(cand_id)
            pos_name = ""
            for p in self.positions:
                if p.id == pos_id:
                    pos_name = p.name
                    break

            if candidate:
                badge = tk.Frame(self.selected_frame, bg=LIGHT_GREEN,
                               relief="solid", borderwidth=1)
                badge.pack(side="left", padx=5, pady=5)
                tk.Label(badge, text=candidate.full_name, font=FONT_SMALL,
                        bg=LIGHT_GREEN, fg=DARK_TEXT).pack(side="top", padx=12, pady=(8, 0))
                tk.Label(badge, text=pos_name, font=FONT_TINY,
                        bg=LIGHT_GREEN, fg=LIGHT_TEXT).pack(side="top", padx=12, pady=(0, 8))
                tk.Button(badge, text="✕", font=("Arial", 8), bg=LIGHT_GREEN, fg=RED,
                         relief="flat", cursor="hand2", borderwidth=0,
                         command=lambda pid=pos_id: self._deselect(pid)).pack(
                    side="right", padx=(0, 8))

    def _submit_votes(self):
        """Submit all selected votes."""
        if not self.selected:
            messagebox.showwarning("No Selection", "Please vote for at least one position.")
            return

        if not messagebox.askyesno("Confirm", "Submit all votes?\nThis cannot be undone."):
            return

        from models.voter import Voter
        from models.vote import Vote

        # Record voter
        voter = Voter(self.voter_email)
        voter.record()

        # Record each vote
        for pos_id, cand_id in self.selected.items():
            candidate = Candidate.get_by_id(cand_id)
            if candidate:
                candidate.increment_vote()
                vote = Vote(self.voter_email, cand_id, pos_id)
                vote.record()

        messagebox.showinfo("Success", "Votes recorded successfully!\nThank you for voting.")
        self.on_submit_complete()