import re
from typing import Dict

class IntentParser:
    def __init__(self):
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
    def parse(self, prompt: str) -> Dict:
        text = self._preprocess(prompt)
        for pattern, handler in self.rules:
            match = re.search(pattern, text)
            if match:
                return handler(match)
        return self._handle_fallback(prompt)
    
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


print(IntentParser().parse("Add two numbers"))
print(IntentParser().parse("Sum 3 numbers"))
print(IntentParser().parse("Add numbers"))
print(IntentParser().parse("Multiply numbers")) 
print(IntentParser().parse("Multiply three numbers"))
print(IntentParser().parse("Product four numbers"))
print(IntentParser().parse("Multiply numbers"))