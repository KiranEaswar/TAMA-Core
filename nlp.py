# nlp.py
import re
from typing import Dict, List

class IntentParser:
    def __init__(self):
        self.rule_categories = {
            'arithmetic': self._arithmetic_rules(),
            'list_operations': self._list_operation_rules(),
            'string_operations': self._string_operation_rules(),
            'comparisons': self._comparison_rules()
        }

    def parse(self, text: str) -> Dict:
        text = self._preprocess(text)
        for category in self.rule_categories.values():
            for pattern, handler in category:
                match = re.search(pattern, text)
                if match:
                    return handler(match)
        return self._handle_fallback(text)

    def _preprocess(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return re.sub(r'\s+', ' ', text)

    # === Arithmetic Rules ===
    def _arithmetic_rules(self) -> List:
        return [
            (r'(add|sum|total)\s+(?:(\w+)\s+)?numbers?', self._handle_addition),
            (r'(multiply|product)\s+(?:(\w+)\s+)?numbers?', self._handle_multiplication),
            (r'subtract\s+(?:(\w+)\s+)?numbers?', self._handle_subtraction),
            (r'divide\s+(?:(\w+)\s+)?numbers?', self._handle_division)
        ]

    def _handle_addition(self, match) -> Dict:
        count = self._parse_count(match.group(2)) or 2
        return self._build_arithmetic_spec('add', count, '+')

    def _handle_multiplication(self, match) -> Dict:
        count = self._parse_count(match.group(2)) or 2
        return self._build_arithmetic_spec('multiply', count, '*')

    def _handle_subtraction(self, match) -> Dict:
        return {
            'name': 'subtract',
            'args': ['a', 'b'],
            'body': 'return a - b'
        }

    def _handle_division(self, match) -> Dict:
        return {
            'name': 'divide',
            'args': ['a', 'b'],
            'body': 'return a / b'
        }

    def _build_arithmetic_spec(self, operation: str, arg_count: int, operator: str) -> Dict:
        args = [f'num{i+1}' for i in range(arg_count)]
        return {
            'name': f'{operation}_{arg_count}_numbers',
            'args': args,
            'body': f'return {f" {operator} ".join(args)}'
        }

    def _parse_count(self, text: str) -> int:
        number_map = {
            'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10
        }
        return number_map.get(text, None)

    # === List Operation Rules ===
    def _list_operation_rules(self) -> List:
        return [
            (r'sort\s+(?:a\s)?list', self._handle_sort_list),
            (r'find\s+(?:the\s)?(max|maximum|min|minimum)\s+in\s+a\s+list', self._handle_list_extremes),
            (r'reverse\s+(?:a\s)?list', self._handle_reverse_list),
            (r'filter\s+list', self._handle_filter_list)
        ]

    def _handle_sort_list(self, match) -> Dict:
        return {
            'name': 'sort_list',
            'args': ['input_list'],
            'body': 'return sorted(input_list)'
        }

    def _handle_list_extremes(self, match) -> Dict:
        operation = match.group(1).lower()
        if operation.startswith('max'):
            op = 'max'
        else:
            op = 'min'
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

    # === String Operation Rules ===
    def _string_operation_rules(self) -> List:
        return [
            (r'reverse\s+string', self._handle_reverse_string),
            (r'uppercase\s+string', self._handle_uppercase),
            (r'lowercase\s+string', self._handle_lowercase)
        ]

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

    # === Comparison Rules ===
    def _comparison_rules(self) -> List:
        return [
            (r'compare\s+two\s+numbers', self._handle_compare_numbers),
            (r'check\s+if\s+equal', self._handle_check_equality)
        ]

    def _handle_compare_numbers(self, match) -> Dict:
        return {
            'name': 'compare_numbers',
            'args': ['a', 'b'],
            'body': 'return "equal" if a == b else ("a > b" if a > b else "a < b")'
        }

    def _handle_check_equality(self, match) -> Dict:
        return {
            'name': 'check_equality',
            'args': ['a', 'b'],
            'body': 'return a == b'
        }

    # === Fallback ===
    def _handle_fallback(self, text: str) -> Dict:
        # Try to guess action and argument count
        verbs = ['add', 'sum', 'multiply', 'sort', 'reverse', 'compare']
        action = next((v for v in verbs if v in text), 'do_nothing')
        numbers = re.findall(r'\b(two|three|four|five|six|seven|eight|nine|ten|\d+)\b', text)
        arg_count = self._parse_count(numbers[0]) if numbers else 1
        return {
            'name': f'{action}_fallback',
            'args': [f'arg{i+1}' for i in range(arg_count)],
            'body': '# Auto-generated\nreturn " ".join(map(str, args))'
        }

# Example usage
if __name__ == "__main__":
    parser = IntentParser()
    tests = [
        "Add two numbers",
        "Sum three values",
        "Multiply four numbers",
        "Sort the list please",
        "Find the maximum in a list",
        "Reverse this string",
        "Uppercase string",
        "Lowercase string",
        "Compare two numbers",
        "Check if equal",
        "Do something with these items"
    ]
    for test in tests:
        result = parser.parse(test)
        print(f"Input: {test}\nOutput: {result}\n{'-'*40}")
