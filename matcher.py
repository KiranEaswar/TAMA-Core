#matcher.py
"""
=====================================================================
|    Module Name   : matcher.py                                     |
|    Description   : Semantic intent matcher using sentence         |
|                    embeddings (MiniLM) and SQLite memory.         |
|                                                                   |
|    Author        : Gengai                                         |
|    Created On    : 2025-06-14                                     |
|    Version       : v1.0                                           |
=====================================================================
"""

import sqlite3
import numpy as np
from typing import Optional, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class IntentMatcher:
    def __init__(self,memdb = 'IntentVault.db'):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = 0.4
        self.db = memdb
    def _fetch_all_prompts(self):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.execute('''
                SELECT prompt FROM IntentVault''')
            return [row[0] for row in cursor.fetchall()]
    def match(self,prompt: str) -> Optional[Tuple[str, float]]:
        prompts = self._fetch_all_prompts()
        if not prompts:
            return None
        embeddings = self.model.encode(prompts + [prompt])
        query_vec = embeddings[-1].reshape(1,-1)
        db_vecs = embeddings[:-1]
        sims = cosine_similarity(query_vec, db_vecs).flatten()
        max_index = int(np.argmax(sims))
        max_score = float(sims[max_index])
        if max_score >= self.threshold:
            return (prompts[max_index], max_score)
        return None

#Example Usage
if __name__ == "__main__":
    matcher = IntentMatcher()
    result = matcher.match("Find square of x")
    if result:
        print(f"[MATCH] Closest intent: '{result[0]}' ({result[1]*100:.2f}%)")
    else:
        print("[MATCH] No good match found.")
    