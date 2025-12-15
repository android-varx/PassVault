import sqlite3
import contextlib
from typing import Generator, Any, List, Tuple, Optional
import os

# Fix path to be absolute relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Moves up one level from src/ to root/
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_NAME = os.path.join(ROOT_DIR, "passvault.db")

class DatabaseManager:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self._initialize_db()

    def _initialize_db(self):
        """Creates the necessary tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Sites table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)
            # Users/Passwords table (Encrypted passwords)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password TEXT NOT NULL,
                    FOREIGN KEY (site_id) REFERENCES sites (id) ON DELETE CASCADE
                )
            """)
            # Config table for Verification Token
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            conn.commit()

    @contextlib.contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Yields a database connection context."""
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def get_config(self, key: str) -> Optional[str]:
        """Retrieves a config value."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    def set_config(self, key: str, value: str):
        """Sets a config value."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
            conn.commit()
            
    def add_site(self, name: str) -> int:
        """Adds a site and returns its ID. Returns existing ID if present."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO sites (name) VALUES (?)", (name,))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # Site already exists, fetch ID
                cursor.execute("SELECT id FROM sites WHERE name = ?", (name,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                raise

    def add_credential(self, site_id: int, username: str, encrypted_password: str):
        """Adds a new credential entry."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO credentials (site_id, username, encrypted_password)
                VALUES (?, ?, ?)
            """, (site_id, username, encrypted_password))
            conn.commit()

    def get_sites(self) -> List[str]:
        """Returns a list of all site names."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sites ORDER BY name ASC")
            return [row[0] for row in cursor.fetchall()]

    def get_credentials(self, site_name: str) -> List[Tuple[int, str, str]]:
        """Returns list of (id, username, encrypted_password) for a given site."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.username, c.encrypted_password
                FROM credentials c
                JOIN sites s ON c.site_id = s.id
                WHERE s.name = ?
            """, (site_name,))
            return cursor.fetchall()

    def update_credential(self, cred_id: int, new_username: str = None, new_encrypted_password: str = None):
        """Updates a credential."""
        if not new_username and not new_encrypted_password:
            return

        with self.get_connection() as conn:
            cursor = conn.cursor()
            if new_username:
                cursor.execute("UPDATE credentials SET username = ? WHERE id = ?", (new_username, cred_id))
            if new_encrypted_password:
                cursor.execute("UPDATE credentials SET encrypted_password = ? WHERE id = ?", (new_encrypted_password, cred_id))
            conn.commit()

    def delete_credential(self, cred_id: int):
        """Deletes a credential."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM credentials WHERE id = ?", (cred_id,))
            conn.commit()

    def delete_site_if_empty(self, site_id: int):
        """Checks if a site has no credentials left and deletes it."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM credentials WHERE site_id = ?", (site_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("DELETE FROM sites WHERE id = ?", (site_id,))
                conn.commit()

    def nuclear_reset(self):
        """Danger: Deletes the entire database file."""
        if os.path.exists(self.db_name):
            try:
                os.remove(self.db_name)
            except PermissionError:
                # On windows/wsl file might be locked if connection matches
                pass 
        # Re-initialize immediately so the file and tables exist for the running app
        self._initialize_db()
