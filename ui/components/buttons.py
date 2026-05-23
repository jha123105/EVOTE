"""
Reusable button components with consistent styling.
Uses inheritance for different button types (OOP polymorphism).
"""
import tkinter as tk
from ui.styles import *


class BaseButton(tk.Button):
    """
    Base button class with common styling and hover effects.
    All specialized buttons inherit from this class.
    """

    def __init__(self, parent, text, color, command, width=BUTTON_WIDTH, font_size=10):
        self.base_color = color
        self.hover_color = self._darken_color(color)

        super().__init__(
            parent,
            text=text,
            bg=color,
            fg="white",
            font=(FONT_FAMILY, font_size, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground=self.hover_color,
            activeforeground="white",
            padx=12,
            pady=6,
            width=width,
            command=command
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _darken_color(self, hex_color):
        """Darken a hex color by reducing each RGB component by 30."""
        hex_color = hex_color.lstrip('#')
        r = max(0, int(hex_color[0:2], 16) - 30)
        g = max(0, int(hex_color[2:4], 16) - 30)
        b = max(0, int(hex_color[4:6], 16) - 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _on_enter(self, event):
        self.configure(bg=self.hover_color)

    def _on_leave(self, event):
        self.configure(bg=self.base_color)


class PrimaryButton(BaseButton):
    """Blue button for main actions like 'Start Voting' or 'Sign In'."""
    def __init__(self, parent, text, command, width=BUTTON_WIDTH, font_size=10):
        super().__init__(parent, text, BLUE, command, width, font_size)


class SuccessButton(BaseButton):
    """Green button for confirm/save/verify actions."""
    def __init__(self, parent, text, command, width=BUTTON_WIDTH, font_size=10):
        super().__init__(parent, text, GREEN, command, width, font_size)


class DangerButton(BaseButton):
    """Red button for delete/reset/logout actions."""
    def __init__(self, parent, text, command, width=BUTTON_WIDTH, font_size=10):
        super().__init__(parent, text, RED, command, width, font_size)


class WarningButton(BaseButton):
    """Orange button for edit/modify actions."""
    def __init__(self, parent, text, command, width=BUTTON_WIDTH, font_size=10):
        super().__init__(parent, text, ORANGE, command, width, font_size)


class GrayButton(BaseButton):
    """Gray button for secondary/browse actions."""
    def __init__(self, parent, text, command, width=BUTTON_WIDTH, font_size=10):
        super().__init__(parent, text, GRAY, command, width, font_size)


class DarkButton(BaseButton):
    """Dark button for admin panel actions."""
    def __init__(self, parent, text, command, width=BUTTON_WIDTH, font_size=10):
        super().__init__(parent, text, BG_DARK, command, width, font_size)


class TextButton(tk.Button):
    """Text-only button with no background (for navigation)."""

    def __init__(self, parent, text, command, color=BLUE):
        super().__init__(
            parent,
            text=text,
            font=(FONT_FAMILY, 10),
            bg=parent['bg'],
            fg=color,
            relief="flat",
            cursor="hand2",
            command=command
        )