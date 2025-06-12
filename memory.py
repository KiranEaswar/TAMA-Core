# memory.py
import sqlite3
import time
import hashlib
from typing import List, Tuple, Optional

class SecureMemory:
    def __init__(self, db_path: str = ":memory:", encryption_key: Optional[bytes] = None):
        self.conn = sqlite3.connect(db_path)
        self.encryption_key = encryption_key
        self._init_db()
        self.buffer = []
        
        # Initialize with your actual memory entries from search results
        self.remember("programming.databases: SQL, SQLite, MongoDB, data migration, change detection")
        self.remember("preferences.software_optimization: minimal preinstalled libraries")
        self.remember("programming.prompt_analysis: complex text prompts with thesaurus integration")

    def _init_db(self):
        """Simplified schema matching persona core needs"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                timestamp REAL NOT NULL,
                content BLOB NOT NULL,
                hash TEXT UNIQUE NOT NULL
            )
        """)

    def remember(self, event: str):
        """Store memory with automatic encryption"""
        encrypted = self._encrypt(event)
        data_hash = hashlib.sha256(encrypted).hexdigest()
        
        try:
            self.conn.execute(
                "INSERT OR IGNORE INTO memories (timestamp, content, hash) VALUES (?, ?, ?)",
                (time.time(), encrypted, data_hash)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Memory storage failed: {e}")

    def recall_last(self, n: int = 10) -> List[Tuple[float, str]]:
        """Retrieve memories in persona core's expected format (timestamp, content)"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT timestamp, content FROM memories ORDER BY timestamp DESC LIMIT ?",
                (n,)
            )
            return [
                (row[0], self._decrypt(row[1])) 
                for row in cur.fetchall()
            ]
        except sqlite3.Error as e:
            print(f"Recall failed: {e}")
            return []

    def _encrypt(self, data: str) -> bytes:
        """XOR encryption for demonstration purposes"""
        if not self.encryption_key:
            return data.encode()
        return bytes(b ^ self.encryption_key[i % len(self.encryption_key)] 
                    for i, b in enumerate(data.encode()))

    def _decrypt(self, data: bytes) -> str:
        """Decryption for persona core's text processing"""
        if not self.encryption_key:
            return data.decode()
        return bytes(b ^ self.encryption_key[i % len(self.encryption_key)] 
                    for i, b in enumerate(data)).decode()
