# PassVault 2.0

PassVault is a secure, modern, and private password manager built with Python.

## Features
- **Modern UI**: Built with CustomTkinter for a sleek dark-mode experience.
- **Secure Encryption**: Uses AES (Fernet) encryption derived from a Master Password (PBKDF2-HMAC-SHA256).
- **Zero Knowledge**: We do not store your master password.
- **Nuclear Reset**: If you forget your password, you can securely wipe the database and start over.
- **Random Password Generator**: Generate strong passwords instantly.

## Installation

### Prerequisites
- Python 3.10 or higher.
- Git.

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/PassVault.git
cd PassVault
```

### 2. Set up a Virtual Environment (Recommended)
**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux/WSL:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install System Dependencies (Linux/WSL Only)
If you are on Linux or WSL, you might need to install Tkinter manually:
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python run.py
```

### First Login
- On the first run, enter any password. This will become your **Master Password**.
- **REMEMBER IT**. There is no recovery if you lose it (except wiping the database).

### Forgot Password?
- Click the "Nuclear Reset" button on the login screen.
- Confirm the warning.
- This will **DELETE ALL DATA** and allow you to set a new master password.

## Project Structure
- `src/`: Source code.
- `src/database.py`: SQLite handling using parameterized queries (SQL injection safe).
- `src/crypto.py`: Encryption logic.
- `src/ui/`: User Interface modules.
- `assets/`: Images and resources.
