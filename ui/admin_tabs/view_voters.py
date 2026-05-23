"""
View Voters tab - Shows which voters voted for which candidates.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.position import Position
from models.candidate import Candidate
from ui.styles import *
from ui.components.buttons import PrimaryButton, GrayButton
from ui.components.labels import HeadingLabel, BaseLabel, SubtitleLabel


class ViewVotersTab(tk.Frame):
    """Tab for viewing voters by position and candidate."""

    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        """Build the view voters UI."""
        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Left sidebar - Positions
        left = tk.Frame(main, bg=BG_WHITE, width=200, relief="solid", borderwidth=1)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        HeadingLabel(left, "Positions").pack(pady=15)

        positions = Position.get_all()
        for pos in positions:
            btn = tk.Button(left, text=pos.name, font=FONT_SMALL,
                          bg=BG_WHITE, fg=DARK_TEXT, relief="flat",
                          cursor="hand2", anchor="w", width=18,
                          command=lambda p=pos: self._load_voters(p))
            btn.pack(pady=2, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=LIGHT_BLUE))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BG_WHITE))

        # Right panel
        self.right = tk.Frame(main, bg=BG_WHITE, relief="solid", borderwidth=1)
        self.right.pack(side="left", fill="both", expand=True, padx=(15, 0))

        # Default message
        BaseLabel(self.right, "Select a position to view voters",
                 font=FONT_NORMAL, fg=LIGHT_TEXT).pack(expand=True)

    def _load_voters(self, position):
        """Load voters for a specific position."""
        for widget in self.right.winfo_children():
            widget.destroy()

        # Header
        header = tk.Frame(self.right, bg=BG_WHITE, height=40)
        header.pack(fill="x", padx=15, pady=(10, 5))
        HeadingLabel(header, f"Voters: {position.name}").pack()

        candidates = Candidate.get_by_position(position.id)

        if not candidates:
            SubtitleLabel(self.right, "No candidates for this position.").pack(expand=True)
            return

        # Create a container frame to hold canvas + scrollbar properly
        container = tk.Frame(self.right, bg=BG_WHITE)
        container.pack(fill="both", expand=True, padx=5, pady=5)

        # Canvas with scrollbar
        canvas = tk.Canvas(container, bg=BG_WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        # Scrollable frame inside canvas
        scroll_frame = tk.Frame(canvas, bg=BG_WHITE)

        # Update scroll region when scroll_frame changes size
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", _on_frame_configure)

        # Create the window inside canvas
        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        # Make the inner frame match canvas width when canvas resizes
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add candidate rows to scrollable frame
        for cand in candidates:
            row = tk.Frame(scroll_frame, bg=BG_WHITE, relief="solid", borderwidth=1)
            row.pack(fill="x", padx=5, pady=3)

            info = tk.Frame(row, bg=BG_WHITE)
            info.pack(side="left", padx=15, pady=10)
            BaseLabel(info, cand.full_name, font=FONT_NORMAL).pack(anchor="w")
            SubtitleLabel(info, f"Votes: {cand.votes}").pack(anchor="w")

            PrimaryButton(row, "View Voters",
                         lambda c=cand: self._show_voters_popup(c),
                         width=12, font_size=9).pack(side="right", padx=15, pady=10)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind mousewheel only when mouse is over the canvas
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def _show_voters_popup(self, candidate):
        """Show a simple popup with the list of voters for a candidate."""
        voters = candidate.get_voters()

        popup = tk.Toplevel(self)
        popup.title(f"Voters: {candidate.full_name}")
        popup.configure(bg=BG_WHITE)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        # Center the popup
        popup.update_idletasks()
        w = 500
        h = 400
        parent = self.winfo_toplevel()
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")

        # Header, fixed at top
        header = tk.Frame(popup, bg=BG_WHITE, height=60)
        header.pack(fill="x", padx=20, pady=(15, 0))
        header.pack_propagate(False)
        HeadingLabel(header, candidate.full_name).pack()
        SubtitleLabel(header, f"Total Votes: {candidate.votes}  |  Voters: {len(voters)}").pack()

        tk.Frame(popup, bg=LIGHT_GRAY, height=1).pack(fill="x", padx=20, pady=(5, 0))

        # Scrollable Content, fills remaining space
        if not voters:
            SubtitleLabel(popup, "No voters have voted for this candidate yet.").pack(expand=True)
        else:
            container = tk.Frame(popup, bg=BG_WHITE)
            container.pack(fill="both", expand=True, padx=20, pady=10)

            canvas = tk.Canvas(container, bg=BG_WHITE, highlightthickness=0)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

            scroll_frame = tk.Frame(canvas, bg=BG_WHITE)

            def _on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            scroll_frame.bind("<Configure>", _on_frame_configure)

            canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

            def _on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)

            canvas.bind("<Configure>", _on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for i, email in enumerate(voters, 1):
                bg = LIGHT_GRAY if i % 2 == 0 else BG_WHITE
                tk.Label(scroll_frame, text=f"  {i}.  {email}",
                        font=FONT_SMALL, bg=bg, fg=DARK_TEXT, anchor="w",
                        height=2).pack(fill="x")

            # Mouse wheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
            canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Divider line 
        tk.Frame(popup, bg=LIGHT_GRAY, height=1).pack(fill="x", padx=20)

        # Close button, fixed at bottom pre
        button_frame = tk.Frame(popup, bg=BG_WHITE, height=50)
        button_frame.pack(fill="x", pady=10)
        button_frame.pack_propagate(False)
        GrayButton(button_frame, "Close", popup.destroy, width=10).pack()

        popup.focus_force()