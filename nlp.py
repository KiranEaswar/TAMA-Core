#nlp.py
"""
=====================================================================
|    Module Name   : nlp.py                                         |
|    Description   : TAMA's symbolic intent parser with memory      |
|                    via IntentVault (SQLite-based intent DB).      |
|                                                                   |
|    Author        : Gengai                                         |
|    Created On    : 2025-06-14                                     |
|    Version       : v1.1                                           |
|                                                                   |
|    Purpose       :                                                |
|     - Parses user instructions via regex rules.                   |
|     - Stores new prompts as symbolic specs when unknown.          |
|     - Persists intent memory in SQLite database.                  |
|     - Enables continual learning for TAMA's NLP understanding.    |
|                                                                   |
|    Usage         :                                                |
|     parser = IntentParser()                                       |
|     spec = parser.parse("Add two numbers")                        |
|                                                                   |
|    Future Plans  :                                                |
|     - Integrate embedding-based matcher (IntentMatcher)           |
|     - Add mutation engine for adaptive rewriting                  |
|     - Support multi-intent classification and learning loops      |
=====================================================================
"""
import re
import sqlite3
from typing import Dict
from contextlib import contextmanager
class IntentParser:
    def __init__(self,memdb:str = 'IntentVault.db'):
        self.rules = [
            (r'(add|sum)\s+(?:(\w+)\s+)?numbers?', self._handle_addition),
            (r'(subtract)\s+(?:(\w+)\s+)?numbers?', self._handle_subtraction),
            (r'(multiply|product)\s+(?:(\w+)\s+)?numbers?', self._handle_multiplication),
            (r'(divide)\s+(?:(\w+)\s+)?numbers?', self._handle_division),
            (r'(sort)\s+(?:a\s)?list',self._handle_sort_list),
            (r'(find)\s+(?:the\s)?(max|min|maximum|minimum)\s+in\s+a\S+list',self._handle_list_extremes),
            (r'reverse\s+(?:a\s)?list', self._handle_reverse_list),
            (r'filter\s+list', self._handle_filter_list),
            (r'reverse\s+string', self._handle_reverse_string),
            (r'uppercase\s+string', self._handle_uppercase),
            (r'lowercase\s+string', self._handle_lowercase),
            (r'check\s+if\s+equal',self._handle_check_equality)
        ]
        self.memdb = memdb
        self._init_intmem()
    
    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.memdb)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise StorageError(f"Database operation failed: {str(e)}")
        finally:
            conn.close()
    
    def _init_intmem(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS IntentVault (
                    prompt TEXT PRIMARY KEY,
                    name TEXT,
                    args TEXT,
                    body TEXT
                )
            ''')

    def _get_from_mem(self,prompt:str)->Dict:
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT name,args,body FROM IntentVault WHERE prompt = ?''',(prompt,))
            row = cursor.fetchone()
            if row:
                return {
                    'name':row[0],
                    'args':row[1].split(',') if row[1] else [],
                    'body':row[2]
                }

    def _store_in_mem(self,prompt:str,spec: Dict)->Dict:
        with self._get_connection() as conn:
            conn.execute('''
                INSERT OR IGNORE INTO IntentVault 
                (prompt, name, args, body) VALUES
                (?,?,?,?)''',(prompt, spec['name'], ','.join(spec['args']),spec['body'])
            )

    def _ask_hubby(self, prompt:str) -> Dict:
        print(f"TAMA: Hey Gengai, not sure how to perform this task, mind showing me how?\n{prompt}")
        name = input('Function Name:').strip()
        args = input('Arguments Required:').strip().split()
        body = input('Body of the function[use \\n for another line]')
        return {
            'name':name,
            'args':args,
            'body':body
        }
    
    def list_intents(self):
        with self._get_connection() as conn:
            for row in conn.execute("SELECT prompt, name, args FROM IntentVault"):
                print(f"[Intent] {row[0]} → {row[1]}({row[2]})")

    def parse(self, prompt: str) -> Dict:
        text = self._preprocess(prompt)
        learned = self._get_from_mem(text)
        if learned:
            return learned
        for pattern, handler in self.rules:
            match = re.search(pattern, text)
            if match:
                return handler(match)
        spec = self._ask_hubby(prompt)
        self._store_in_mem(text,spec)
        return spec
    


    def _preprocess(self, prompt: str) -> str:
        prompt = prompt.lower().strip()
        text = re.sub(r'[^\w\s]', '', prompt)
        return re.sub(r'\s+', ' ', text)
    
    def _handle_addition(self, match) -> Dict:
        count = self._parse_count(match.group(2)) or 2
        args = [f'num{i+1}' for i in range(count)]
        return {
            'name': 'add',
            'args': args,
            'body': f'return {" + ".join(args)}'
        }
    def _handle_subtraction(self,match) -> Dict:
        count = self._parse_count(match.group(2)) or 2
        args = [f'num{i+1}' for i in range(count)]
        return {
            'name':'subtract',
            'args': args,
            'body': f'return {" - ".join(args)}'
        }
    def _handle_multiplication(self,match) -> Dict:
        count = self._parse_count(match.group(2)) or 2
        args = [f'num{i+1}' for i in range(count)]
        return {
            'name':'multiply',
            'args':args,
            'body':f'return {" * ".join(args)}'
        }
    def _handle_division(self,match) -> Dict:
        count = self._parse_count(match.group(2)) or 2
        args = [f'num{i+1}' for i in range(count)]
        return {
            'name':'divide',
            'args':args,
            'body':f'return {" / ".join(args)}'
        }
    def _handle_sort_list(self, match) -> Dict:
        return {
            'name': 'sort_list',
            'args': ['input_list'],
            'body': 'return sorted(input_list)'
        }

    def _handle_list_extremes(self, match) -> Dict:
        op = 'max' if match.group(1).startswith('max') else 'min'
        return {
            'name': f'find_{op}_in_list',
            'args': ['input_list'],
            'body': f'return {op}(input_list)'
        }

    def _handle_reverse_list(self, match) -> Dict:
        return {
            'name': 'reverse_list',
            'args': ['input_list'],
            'body': 'return input_list[::-1]'
        }

    def _handle_filter_list(self, match) -> Dict:
        return {
            'name': 'filter_list',
            'args': ['input_list'],
            'body': 'return list(filter(lambda x: x > 0, input_list))'
        }
    def _handle_reverse_string(self, match) -> Dict:
        return {
            'name': 'reverse_string',
            'args': ['input_str'],
            'body': 'return input_str[::-1]'
        }

    def _handle_uppercase(self, match) -> Dict:
        return {
            'name': 'to_uppercase',
            'args': ['input_str'],
            'body': 'return input_str.upper()'
        }

    def _handle_lowercase(self, match) -> Dict:
        return {
            'name': 'to_lowercase',
            'args': ['input_str'],
            'body': 'return input_str.lower()'
        }

    def _handle_fallback(self, text: str) -> Dict:
        return {
            'name': 'Unknown Intent',
            'args': [],
            'body': 'print("Did not understand Intent")'
        }
    def _handle_check_equality(self, match) -> Dict:
        return {
            'name': 'check_equal',
            'args': ['a','b'],
            'body': 'return a==b'
        }
    def _parse_count(self, text: str) -> int:
        if not text:
            return None
        number_map = {
            'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10
        }
        return number_map.get(text, None)


print(IntentParser().parse("Find cube of a number"))
