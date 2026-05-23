"""
View Results tab - Shows election standings and winners.
Exports categorized PDF by position with overall standings.
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from models.position import Position
from models.candidate import Candidate
from ui.styles import *
from ui.components.buttons import DangerButton, GrayButton
from ui.components.labels import HeadingLabel, BaseLabel, SubtitleLabel


class ViewResultsTab(tk.Frame):
    """Tab for viewing election results."""

    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        """Build the view results UI."""
        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Top bar
        top = tk.Frame(main, bg=BG_WHITE, height=40, relief="solid", borderwidth=1)
        top.pack(fill="x", pady=(0, 10))
        top.pack_propagate(False)
        HeadingLabel(top, "Election Results").pack(side="left", padx=15)
        DangerButton(top, "Export PDF", self._export_pdf, width=12, font_size=9).pack(
            side="right", padx=10, pady=5)

        # Left sidebar - Positions
        left = tk.Frame(main, bg=BG_WHITE, width=200, relief="solid", borderwidth=1)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        HeadingLabel(left, "Positions").pack(pady=15)

        # "Overall" button
        btn = tk.Button(left, text="Overall Standings", font=FONT_SMALL,
                      bg=LIGHT_BLUE, fg=BLUE, relief="flat",
                      cursor="hand2", anchor="w", width=18,
                      command=self._show_overall)
        btn.pack(pady=2, padx=10)

        # Position buttons
        positions = Position.get_all()
        for pos in positions:
            btn = tk.Button(left, text=pos.name, font=FONT_SMALL,
                          bg=BG_WHITE, fg=DARK_TEXT, relief="flat",
                          cursor="hand2", anchor="w", width=18,
                          command=lambda p=pos: self._show_results(p))
            btn.pack(pady=2, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=LIGHT_BLUE))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BG_WHITE))

        # Right panel
        self.right = tk.Frame(main, bg=BG_WHITE, relief="solid", borderwidth=1)
        self.right.pack(side="left", fill="both", expand=True, padx=(15, 0))

        self._show_overall()

    def _show_overall(self):
        """Show overall standings across all positions."""
        for widget in self.right.winfo_children():
            widget.destroy()

        HeadingLabel(self.right, "Overall Standings").pack(pady=15)

        results = Candidate.get_all()
        if not results:
            SubtitleLabel(self.right, "No votes cast yet").pack(expand=True)
            return

        for i, cand in enumerate(results):
            is_winner = (i == 0)
            bg = LIGHT_GREEN if is_winner else (BG_WHITE if i % 2 == 0 else LIGHT_GRAY)

            row = tk.Frame(self.right, bg=bg, height=35)
            row.pack(fill="x")
            row.pack_propagate(False)

            prefix = "👑 " if is_winner else f"#{i + 1} "
            pos_name = getattr(cand, 'position_name', '')
            tk.Label(row, text=f"{prefix}{cand.full_name} ({pos_name})",
                    font=FONT_NORMAL, bg=bg,
                    fg=GREEN if is_winner else DARK_TEXT).pack(side="left", padx=15)
            tk.Label(row, text=f"{cand.votes} votes",
                    font=FONT_NORMAL, bg=bg,
                    fg=GREEN if is_winner else DARK_TEXT).pack(side="right", padx=15)

    def _show_results(self, position):
        """Show results for a specific position."""
        for widget in self.right.winfo_children():
            widget.destroy()

        HeadingLabel(self.right, f"Results: {position.name}").pack(pady=15)

        candidates = Candidate.get_by_position(position.id)
        candidates.sort(key=lambda c: c.votes, reverse=True)

        if not candidates:
            SubtitleLabel(self.right, "No candidates").pack(expand=True)
            return

        for i, cand in enumerate(candidates):
            is_winner = (i == 0)
            bg = LIGHT_GREEN if is_winner else (BG_WHITE if i % 2 == 0 else LIGHT_GRAY)

            row = tk.Frame(self.right, bg=bg, height=35)
            row.pack(fill="x")
            row.pack_propagate(False)

            prefix = "👑 " if is_winner else f"#{i + 1} "
            tk.Label(row, text=f"{prefix}{cand.full_name}",
                    font=FONT_NORMAL, bg=bg,
                    fg=GREEN if is_winner else DARK_TEXT).pack(side="left", padx=15)
            tk.Label(row, text=f"{cand.votes} votes",
                    font=FONT_NORMAL, bg=bg,
                    fg=GREEN if is_winner else DARK_TEXT).pack(side="right", padx=15)

    def _export_pdf(self):
        """
        Export results to a categorized PDF:
        - Separate table for each position (President, VP, Secretary, etc.)
        - Overall standings table at the bottom
        - Asks to view the PDF after export
        """
        try:
            from reportlab.lib import colors as rl_colors
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                           Paragraph, Spacer, PageBreak)
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
        except ImportError:
            messagebox.showerror("Error", "Install reportlab: pip install reportlab")
            return

        # Check if there's any data
        all_results = Candidate.get_all()
        if not all_results:
            messagebox.showwarning("No Data", "No votes cast yet")
            return

        file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile="Election_Results.pdf"
        )
        if not file:
            return

        try:
            doc = SimpleDocTemplate(file, pagesize=letter,
                                   topMargin=0.5*inch, bottomMargin=0.5*inch)
            story = []
            styles = getSampleStyleSheet()

            #  Title 
            story.append(Paragraph("E-Vote Election Results", styles['Title']))
            story.append(Spacer(1, 10))
            story.append(Paragraph(
                f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
                styles['Normal']
            ))
            
           
            story.append(Spacer(1, 25))


            # Per-Position Tables 
            positions = Position.get_all()
    
            for position in positions:
                # Position header
                story.append(Paragraph(
                    f"Position: {position.name}",
                    styles['Heading2']
                ))
                story.append(Spacer(1, 10))

                candidates = Candidate.get_by_position(position.id)
                candidates.sort(key=lambda c: c.votes, reverse=True)

                if not candidates:
                    story.append(Paragraph(
                        "<i>No candidates for this position.</i>",
                        styles['Normal']
                    ))
                    story.append(Spacer(1, 15))
                    continue

                # Build table data
                table_data = [['Rank', 'Candidate Name', 'Votes', 'Status']]
                for i, cand in enumerate(candidates):
                    rank = i + 1
                    status = "🏆 WINNER" if i == 0 else f"#{rank}"
                    table_data.append([str(rank), cand.full_name, str(cand.votes), status])

                # Create table
                col_widths = [0.5*inch, 3.5*inch, 1*inch, 1.5*inch]
                table = Table(table_data, colWidths=col_widths)

                table.setStyle(TableStyle([
                    # Header
                    ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#4a90d9')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    # Winner row
                    ('BACKGROUND', (0, 1), (-1, 1), rl_colors.HexColor('#e8f8e8')),
                    ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
                    # Alternating rows
                    ('ROWBACKGROUNDS', (0, 2), (-1, -1),
                     [rl_colors.white, rl_colors.HexColor('#f8f9fa')]),
                    # Borders
                    ('GRID', (0, 0), (-1, -1), 1, rl_colors.HexColor('#e0e0e0')),
                    # Alignment
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                    ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                    # Font
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                ]))

                story.append(table)

                # Winner announcement
                winner = candidates[0]
                story.append(Spacer(1, 10))
                story.append(Paragraph(
                    f"<b>Winner:</b> {winner.full_name} — {winner.votes} vote(s)",
                    styles['Normal']
                ))
                

                story.append(Spacer(1, 25))

            # Page break before overall standings
            story.append(PageBreak())

            #  Overall Standings 
            story.append(Paragraph("Overall Standings", styles['Title']))
            story.append(Spacer(1, 15))
            story.append(Paragraph(
                "(All candidates ranked by total votes across all positions)",
                styles['Normal']
            ))
            
            story.append(Spacer(1, 15))

            overall_data = [['Rank', 'Candidate', 'Position', 'Votes']]
            for i, cand in enumerate(all_results):
                rank = i + 1
                pos_name = getattr(cand, 'position_name', 'Unknown')
                overall_data.append([str(rank), cand.full_name, pos_name, str(cand.votes)])

            col_widths2 = [0.5*inch, 3*inch, 2*inch, 1*inch]
            overall_table = Table(overall_data, colWidths=col_widths2)
            overall_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#1a1a2e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                 [rl_colors.white, rl_colors.HexColor('#f8f9fa')]),
                ('GRID', (0, 0), (-1, -1), 1, rl_colors.HexColor('#e0e0e0')),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))
            story.append(overall_table)

            # Top voter turnout
            story.append(Spacer(1, 25))
            total_votes = sum(c.votes for c in all_results)
            story.append(Paragraph(
                f"<b>Total Votes Cast:</b> {total_votes}",
                styles['Normal']
            ))

            # Build PDF
            doc.build(story)

            # Ask to view the PDF 
            view = messagebox.askyesno(
                "Export Successful",
                f"PDF exported successfully!\n\n"
                f"Saved to:\n{file}\n\n"
                f"Do you want to view the results now?"
            )
            if view:
                import os
                os.startfile(file)  # Opens PDF with default viewer

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF:\n{str(e)}")