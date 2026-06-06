# PassVault 3.0

PassVault is a secure, private, and extremely polished password manager built with Python and CustomTkinter. 

Version 3.0 features a premium modern UI design, advanced security audits, automatic timeouts, clipboard clearing, and database backups.

---

## What's New in V3.0

### 🎨 Premium UI & Custom Theme
* **Obsidian & Purple Theme**: Restyled with a custom dark-mode theme utilizing neon violet highlights, custom card widgets, and clean typography.
* **Navigation Sidebar**: A persistent, elegant sidebar to navigate between views seamlessly without clunky screen rebuilds.
* **Inline Cards**: View all passwords in visual cards featuring site categories, inline quick copy buttons, eye icon visibility toggles, and edit actions.

### 🛡️ Enhanced Security
* **Vault Security Auditor**: Calculates a real-time Security Score based on password strength, reuse across different accounts, and age.
* **CSPRNG Password Generator**: Uses Python's cryptographically secure `secrets` library instead of pseudo-random methods.
* **Inactivity Auto-Lock**: Automatically locks the vault and displays the Login screen if no activity occurs for 5 minutes.
* **Auto-Clipboard Clear**: Erases copied usernames or passwords from the system clipboard after 30 seconds.
* **Master Password Checklist**: Enforces complexity (12+ characters, containing uppercase, numbers, and symbols) during setup.
* **Self-Contained DB Salt**: Migrates the legacy file-based `salt.key` into the SQLite database config table to make backups portable.

### ⚡ Power Features
* **Interactive Generator**: Dedicated view to generate passwords from 8 to 64 characters with options to exclude confusing ambiguous characters (e.g. `l`, `1`, `I`, `0`, `O`).
* **Category Filters**: Filter passwords using segmented categories: *Personal, Work, Social, Finance, and Other*.
* **Backup & Restore**: Export the entire database into a strong AES-encrypted JSON file using a key derived from a custom backup password, or import backups to merge credentials.
* **Master Password Transition**: Securely update the master password, which automatically decrypts, re-salts, and re-encrypts every credential in the database.

---

## Architecture

```
src/
  ├── core/               # Vault business logic & database
  │    ├── crypto.py      # AES encryption, key derivation, and salt migration
  │    ├── database.py    # SQLite connections, queries, and schema migrations
  │    └── security.py    # Password strength check & vault security scans
  ├── ui/                 # UI Framework
  │    ├── app.py         # Main CustomTkinter window, timer and event binds
  │    ├── theme.json     # Custom Obsidian & Neon color theme
  │    └── views/         # Panel subviews
  │         ├── login.py  # Setup & unlock screens
  │         ├── home.py   # Shell frame with Sidebar
  │         ├── dashboard.py # Metrics & security actions list
  │         ├── view.py   # Passwords manager, Search, Category Tabs, and Edit dialog
  │         ├── add.py    # Credentials insertion form
  │         ├── generator.py # Standalone password generator
  │         └── settings.py  # Master password change, JSON backup/restore
  └── utils/              # Helper utilities
       └── helpers.py     # Secrets choices and timed clipboard clearing
```

---

## Installation

### Prerequisites
* Python 3.9 or higher.
* Git.

### 1. Clone & Navigate
```bash
git clone https://github.com/YOUR_USERNAME/PassVault.git
cd PassVault
```

### 2. Set up Virtual Environment
**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(On Linux/WSL, you might need to install Tkinter: `sudo apt-get install python3-tk`)*

---

## Usage

Run the app:
```bash
python run.py
```

### Key Operations
* **Setup**: Enter a strong password to initialize the vault. Keep it safe, there is no password reset without deleting all data.
* **Search**: Use the real-time search field on the **My Passwords** view.
* **Audit**: Open the **Dashboard** to see which passwords need update. Click **Fix** to jump directly to the credential.
* **Backup**: Go to **Settings** -> **Export Encrypted JSON** to back up your vault.
* **Nuclear Reset**: Click **Nuclear Reset** on the login screen if you wish to wipe the database and start fresh.
