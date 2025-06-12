# generator.py

class CodeGenerator:
    """
    Converts a function spec into Python code.
    """

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
