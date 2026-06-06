import sqlite3
import contextlib
from typing import Generator, List, Tuple, Optional
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # src/core
SRC_DIR = os.path.dirname(BASE_DIR)                  # src
ROOT_DIR = os.path.dirname(SRC_DIR)                  # root
DB_NAME = os.path.join(ROOT_DIR, "passvault.db")

class DatabaseManager:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self._initialize_db()
        self._migrate_db()

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
            
            # Credentials table (V2 schema)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password TEXT NOT NULL,
                    FOREIGN KEY (site_id) REFERENCES sites (id) ON DELETE CASCADE
                )
            """)
            
            # Config table for Verification Token and Salt
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            conn.commit()

    def _migrate_db(self):
        """Checks schema and migrates database to V3.0 (adding category, created_at, updated_at)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check existing columns in credentials
            cursor.execute("PRAGMA table_info(credentials)")
            columns = [info[1] for info in cursor.fetchall()]
            
            # Add category column if it doesn't exist
            if "category" not in columns:
                cursor.execute("ALTER TABLE credentials ADD COLUMN category TEXT DEFAULT 'Other'")
            
            # Add created_at column if it doesn't exist
            if "created_at" not in columns:
                current_time = datetime.now().isoformat()
                cursor.execute(f"ALTER TABLE credentials ADD COLUMN created_at TEXT DEFAULT '{current_time}'")
                
            # Add updated_at column if it doesn't exist
            if "updated_at" not in columns:
                current_time = datetime.now().isoformat()
                cursor.execute(f"ALTER TABLE credentials ADD COLUMN updated_at TEXT DEFAULT '{current_time}'")
                
            conn.commit()

    @contextlib.contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Yields a database connection context."""
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON") # Enable foreign key support
        try:
            yield conn
        finally:
            conn.close()

    # Config Methods
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

    # Salt Methods (migration of salt from salt.key file to DB config table)
    def get_salt(self) -> Optional[bytes]:
        """Retrieves salt from DB (returned as bytes)."""
        val = self.get_config("salt")
        if val:
            import base64
            return base64.b64decode(val.encode('utf-8'))
        return None

    def set_salt(self, salt_bytes: bytes):
        """Saves salt to DB config as base64 string."""
        import base64
        val_str = base64.b64encode(salt_bytes).decode('utf-8')
        self.set_config("salt", val_str)

    # Site Methods
    def add_site(self, name: str) -> int:
        """Adds a site and returns its ID. Returns existing ID if present."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO sites (name) VALUES (?)", (name,))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                cursor.execute("SELECT id FROM sites WHERE name = ?", (name,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                raise

    def get_sites(self) -> List[str]:
        """Returns a list of all site names that contain active credentials."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT s.name FROM sites s
                JOIN credentials c ON c.site_id = s.id
                ORDER BY s.name ASC
            """)
            return [row[0] for row in cursor.fetchall()]

    # Credential Methods
    def add_credential(self, site_id: int, username: str, encrypted_password: str, category: str = "Other") -> int:
        """Adds a new credential entry and returns its ID."""
        current_time = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO credentials (site_id, username, encrypted_password, category, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (site_id, username, encrypted_password, category, current_time, current_time))
            conn.commit()
            return cursor.lastrowid

    def get_credentials(self, site_name: str) -> List[Tuple[int, str, str, str, str, str]]:
        """Returns list of (id, username, encrypted_password, category, created_at, updated_at) for a given site."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.username, c.encrypted_password, c.category, c.created_at, c.updated_at
                FROM credentials c
                JOIN sites s ON c.site_id = s.id
                WHERE s.name = ?
                ORDER BY c.username ASC
            """, (site_name,))
            return cursor.fetchall()

    def get_all_credentials(self) -> List[Tuple[int, str, str, str, str, str, str]]:
        """Returns list of all credentials: (id, site_name, username, encrypted_password, category, created_at, updated_at)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, s.name, c.username, c.encrypted_password, c.category, c.created_at, c.updated_at
                FROM credentials c
                JOIN sites s ON c.site_id = s.id
                ORDER BY s.name ASC, c.username ASC
            """)
            return cursor.fetchall()

    def search_credentials(self, query: str, category: str = "All") -> List[Tuple[int, str, str, str, str, str, str]]:
        """Searches site names and usernames matching the query and category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT c.id, s.name, c.username, c.encrypted_password, c.category, c.created_at, c.updated_at
                FROM credentials c
                JOIN sites s ON c.site_id = s.id
                WHERE (s.name LIKE ? OR c.username LIKE ?)
            """
            params = [f"%{query}%", f"%{query}%"]
            if category != "All":
                sql += " AND c.category = ?"
                params.append(category)
            sql += " ORDER BY s.name ASC, c.username ASC"
            cursor.execute(sql, params)
            return cursor.fetchall()

    def get_credentials_by_category(self, category: str) -> List[Tuple[int, str, str, str, str, str, str]]:
        """Returns list of all credentials in a category: (id, site_name, username, encrypted_password, category, created_at, updated_at)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, s.name, c.username, c.encrypted_password, c.category, c.created_at, c.updated_at
                FROM credentials c
                JOIN sites s ON c.site_id = s.id
                WHERE c.category = ?
                ORDER BY s.name ASC, c.username ASC
            """, (category,))
            return cursor.fetchall()

    def update_credential(self, cred_id: int, new_site_name: str = None, new_username: str = None, 
                          new_encrypted_password: str = None, new_category: str = None):
        """Updates a credential, handles site association change if new_site_name is provided."""
        current_time = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Fetch current credential to find current site_id
            cursor.execute("SELECT site_id FROM credentials WHERE id = ?", (cred_id,))
            row = cursor.fetchone()
            if not row:
                return
            old_site_id = row[0]

            if new_site_name:
                # Add/Resolve new site ID
                new_site_name_normalized = new_site_name.strip().title()
                # Run add_site logic directly in this transaction to update safely
                cursor.execute("INSERT OR IGNORE INTO sites (name) VALUES (?)", (new_site_name_normalized,))
                cursor.execute("SELECT id FROM sites WHERE name = ?", (new_site_name_normalized,))
                new_site_id = cursor.fetchone()[0]
                cursor.execute("UPDATE credentials SET site_id = ? WHERE id = ?", (new_site_id, cred_id))

            if new_username is not None:
                cursor.execute("UPDATE credentials SET username = ? WHERE id = ?", (new_username.strip(), cred_id))

            if new_encrypted_password is not None:
                cursor.execute("UPDATE credentials SET encrypted_password = ? WHERE id = ?", (new_encrypted_password, cred_id))

            if new_category is not None:
                cursor.execute("UPDATE credentials SET category = ? WHERE id = ?", (new_category, cred_id))

            # Update timestamp
            cursor.execute("UPDATE credentials SET updated_at = ? WHERE id = ?", (current_time, cred_id))
            conn.commit()

            # Clean up old site if it has no credentials left
            if new_site_name and old_site_id != new_site_id:
                self.delete_site_if_empty(old_site_id)

    def delete_credential(self, cred_id: int):
        """Deletes a credential and cleans up site if empty."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Find site_id first
            cursor.execute("SELECT site_id FROM credentials WHERE id = ?", (cred_id,))
            row = cursor.fetchone()
            if not row:
                return
            site_id = row[0]
            
            # Delete credential
            cursor.execute("DELETE FROM credentials WHERE id = ?", (cred_id,))
            conn.commit()
            
        # Clean up site if empty
        self.delete_site_if_empty(site_id)

    def delete_site_if_empty(self, site_id: int):
        """Checks if a site has no credentials left and deletes it."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM credentials WHERE site_id = ?", (site_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("DELETE FROM sites WHERE id = ?", (site_id,))
                conn.commit()

    def nuclear_reset(self):
        """Danger: Deletes the entire database file and starts fresh."""
        if os.path.exists(self.db_name):
            try:
                os.remove(self.db_name)
            except PermissionError:
                pass
        self._initialize_db()
        self._migrate_db()
