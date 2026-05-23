"""
Reusable label components with consistent styling.
"""
import tkinter as tk
from ui.styles import *


class BaseLabel(tk.Label):
    """Base label with common font settings."""

    def __init__(self, parent, text, font=FONT_NORMAL, fg=DARK_TEXT, bg=None):
        if bg is None:
            bg = parent['bg']
        super().__init__(parent, text=text, font=font, bg=bg, fg=fg)


class TitleLabel(BaseLabel):
    """Large bold title (e.g., screen headers)."""
    def __init__(self, parent, text):
        super().__init__(parent, text, font=FONT_TITLE)


class HeadingLabel(BaseLabel):
    """Medium bold heading."""
    def __init__(self, parent, text):
        super().__init__(parent, text, font=FONT_HEADING)


class SubtitleLabel(BaseLabel):
    """Small gray subtitle text."""
    def __init__(self, parent, text):
        super().__init__(parent, text, font=FONT_SMALL, fg=LIGHT_TEXT)


class LargeTitleLabel(BaseLabel):
    """Extra large title for main menu."""
    def __init__(self, parent, text):
        super().__init__(parent, text, font=FONT_LARGE, fg=BLUE)


class WinnerLabel(BaseLabel):
    """Green label for displaying winners."""
    def __init__(self, parent, text):
        super().__init__(parent, text, font=FONT_HEADING, fg=GREEN)