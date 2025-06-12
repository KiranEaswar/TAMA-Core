import sqlite3
import hashlib
from contextlib import contextmanager
from typing import Optional, Dict

class PatchStorage:
    def __init__(self, db_path: str = 'bot_patches.db'):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise StorageError(f"Database operation failed: {str(e)}")
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS patches (
                    hash TEXT PRIMARY KEY,
                    code TEXT NOT NULL,
                    dependencies TEXT,
                    created_at REAL DEFAULT (STRFTIME('%s','now')),
                    last_accessed REAL
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_hash ON patches (hash)')

    def store_patch(self, code: str, dependencies: list = None) -> str:
        func_hash = hashlib.sha256(code.encode()).hexdigest()
        with self._get_connection() as conn:
            conn.execute('''
                INSERT OR IGNORE INTO patches 
                (hash, code, dependencies, last_accessed)
                VALUES (?, ?, ?, STRFTIME('%s','now'))
            ''', (func_hash, code, ','.join(dependencies) if dependencies else None))
        return func_hash

    def get_patch(self, func_hash: str) -> Optional[Dict]:
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT code, dependencies 
                FROM patches 
                WHERE hash = ?
            ''', (func_hash,))
            result = cursor.fetchone()
            if result:
                conn.execute('''
                    UPDATE patches
                    SET last_accessed = STRFTIME('%s','now')
                    WHERE hash = ?
                ''', (func_hash,))
                return {
                    'code': result[0],
                    'dependencies': result[1].split(',') if result[1] else []
                }
        return None

    def patch_exists(self, func_hash: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT 1 
                FROM patches 
                WHERE hash = ?
                LIMIT 1
            ''', (func_hash,))
            return cursor.fetchone() is not None

class StorageError(Exception):
    pass

# Example usage
if __name__ == "__main__":
    storage = PatchStorage()
    sample_code = "def greet():\n    return 'Hello from TAMA!'"
    patch_hash = storage.store_patch(sample_code, ['os'])
    print(f"Stored patch with hash: {patch_hash}")
    print(f"Exists check: {storage.patch_exists(patch_hash)}")
    print(f"Retrieved patch: {storage.get_patch(patch_hash)}")
