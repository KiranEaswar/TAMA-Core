# generator.py
"""
=====================================================================
|    Module Name   : generator.py                                   |
|    Description   : Generates Python function code from structured |
|                    intent specification dictionaries.             |
|                                                                   |
|    Author        : Gengai                                         |
|    Created On    : 2025-06-14                                     |
|    Version       : v1.0                                           |
|                                                                   |
|    Purpose       :                                                |
|     - Translate parsed intent specs into Python code strings.     |
|     - Format function name, arguments, and body.                  |
|                                                                   |
|    Usage         :                                                |
|     code = CodeGenerator().generate(spec)                         |
|                                                                   |
|    Future Plans  :                                                |
|     - Support multi-line body handling.                           |
|     - Add return type annotations and docstring injection.        |
=====================================================================
"""
class CodeGenerator:
    def generate(self, spec: dict) -> str:
        args = ', '.join(['self'] + spec['args'])
        code = f"def {spec['name']}({args}):\n"
        for line in spec['body'].split('\n'):
            code += f"    {line.strip()}\n"
        return code

# Example usage
if __name__ == "__main__":
    generator = CodeGenerator()
    spec = {
        'name': 'add',
        'args': ['a', 'b'],
        'body': 'return a + b'
    }
    print(generator.generate(spec))
