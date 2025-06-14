#storage.py
"""
=====================================================================
|    Module Name   : storage.py                                     |
|    Description   : Manages persistent patch storage for TAMA.     |
|                    Uses SHA-256 hashing and SQLite for tracking   |
|                    user-taught functions and their metadata.      |
|                                                                   |
|    Author        : Gengai                                         |
|    Created On    : 2025-06-14                                     |
|    Version       : v1.1                                           |
|                                                                   |
|    Purpose       :                                                |
|     - Store and retrieve code patches using a content hash.       |
|     - Track dependencies, usage timestamps, and patch integrity.  |
|     - Abstract DB connection logic with context manager.          |
|                                                                   |
|    Usage         :                                                |
|     storage = PatchStorage()                                      |
|     hash = storage.store_patches(code, ['math'])                  |
|     patch = storage.retrieve_patches(hash)                        |
|                                                                   |
|    Future Plans  :                                                |
|     - Plans to add version control for libraries for each patch   |
|     - Enable patch expiration or TTL policies.                    |
|     - Sync patches across multiple agents/devices.                |
=====================================================================
"""
import sqlite3
import hashlib
from typing import Optional,Dict
from contextlib import contextmanager
import logging
#==========[Logging Configs]========
logging.basicConfig(
    filename = "Storage_Errors.log",
    level = logging.ERROR,
    format = '%(asctime)s [%(levelname)s] %(message)s'
)

class PatchStorage:
    def __init__(self, db_path: str = "PatchVault.db"):
        self.db = db_path
        self.logger = logging.getLogger(__name__)
        self._init_db()
    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            self.logger.error("Error at _get_connection()",exc_info = True)
            conn.rollback()
            raise StorageError(f'The Storage broke due to {e}')
        finally:
            conn.close()
    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS PatchVault  (
                    hash TEXT PRIMARY KEY,
                    dependency TEXT,
                    code TEXT NOT NULL,
                    created_at REAL DEFAULT (STRFTIME('%s','now')),
                    last_used REAL)''')
    def store_patches(self,code: str,dependencies: list = None) -> str:
        fash = hashlib.sha256(code.encode()).hexdigest()
        with self._get_connection() as conn:
            conn.execute(
                '''INSERT OR IGNORE INTO PatchVault 
                (hash, dependency, code, last_used) VALUES 
                (?,?,?,STRFTIME('%s','now'))''',
                (fash,','.join(dependencies) if dependencies else None,code)
            )
        return fash
    def retrieve_patches(self, fash: str) -> Optional[Dict]:
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT code, dependency
                FROM PatchVault
                WHERE hash = ?''',(fash,)
                )
            result = cursor.fetchone()
            if result:
                conn.execute('''
                    UPDATE PatchVault
                    SET last_used = STRFTIME('%s','now')
                    WHERE hash = ?''',(fash,)
                )
                return {
                    'code':result[0],
                    'dependencies':result[1].split(',') if result[1] else []
                    }
            return None
    def check_patch(self, fash: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT code, dependency
                FROM PatchVault
                WHERE hash = ?''',(fash,))
            return cursor.fetchone() is not None

#========[StorageError Class]========
class StorageError(Exception):
    pass

#========[Testcases]=================
if __name__ == "__main__":
    storage = PatchStorage()
    sample_code = "def greet():\n    return 'Hello from TAMA!'"
    patch_hash = storage.store_patches(sample_code, ['os'])
    print(f"Stored patch with hash: {patch_hash}")
    print(f"Exists check: {storage.check_patch(patch_hash)}")
    print(f"Retrieved patch: {storage.retrieve_patches(patch_hash)}")
