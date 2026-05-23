# E-Vote System

A GUI-based School Election Management System built with Python and Tkinter.  
E-Vote replaces traditional paper ballots with a secure and automated digital voting platform.

---

## Features

- **Email Verification** – Only valid school email addresses are allowed to vote.
- **Multi-Position Voting** – Supports President, Vice President, Secretary, and custom positions.
- **Candidate Management** – Add, edit, and delete candidates with photo upload support.
- **Real-Time Results** – Automatic vote counting with winner highlighting.
- **PDF Export** – Generates professional election reports organized by position.
- **Admin Management** – Supports multiple administrator accounts with password protection.
- **Election Reset** – Clears votes and voter records while preserving the election setup.

---

## User Roles

| Role | Functions |
|------|-----------|
| **Voter (Student)** | Verify school email, browse candidates, select candidates, and submit votes |
| **Administrator** | Manage candidates and positions, view voters and results, export PDF reports, manage admin accounts, and reset the election |

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Main programming language |
| Tkinter / ttk | Graphical User Interface (GUI) |
| SQLite3 | Database management |
| Pillow (PIL) | Candidate photo handling |
| ReportLab | PDF report generation |
| Regular Expressions | Email validation |
| VS Code | Code editor |

---

## Project Structure

```text
EVOTE/
├── main.py                     # Application entry point
├── database.py                 # Database initialization and sample data
├── models/                     # Data model classes (OOP)
│   ├── position.py
│   ├── candidate.py
│   ├── voter.py
│   ├── admin.py
│   └── vote.py
├── ui/                         # User interface package
│   ├── app.py                  # Main application class
│   ├── styles.py               # Colors, fonts, and dimensions
│   ├── components/             # Reusable UI components
│   │   ├── buttons.py
│   │   ├── labels.py
│   │   ├── cards.py
│   │   └── dialogs.py
│   ├── screens/                # Main screens
│   │   ├── main_menu.py
│   │   ├── verification.py
│   │   ├── voter_panel.py
│   │   ├── admin_login.py
│   │   └── admin_dashboard.py
│   └── admin_tabs/             # Dashboard tab components
│       ├── manage_candidates.py
│       ├── view_voters.py
│       ├── view_results.py
│       └── manage_admins.py
└── assets/                     # Static resources
    ├── logo.png
    └── candidates/             # Candidate photos
```

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/EVOTE.git
cd EVOTE
```

### 2. Install Dependencies

```bash
pip install pillow reportlab
```

### 3. Run the Application

```bash
python main.py
```

or

```bash
py main.py
```

---

## Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |

---

## Team Members

- Josh A.
- Kurt L.
- Dennis G.

---

## License

This project was created for **IT 5/L (8437) – IT Elective 2** at the **University of Mindanao**.

This project is intended for educational purposes only.