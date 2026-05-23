"""
E-Vote System - Main Entry Point
Launches the voting application for school elections.
"""
from database import initialize_database
from ui.app import App


def main():
    """Initialize database and start the application."""
    initialize_database()
    app = App()
    app.run()


if __name__ == "__main__":
    main()