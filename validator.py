# validator.py
"""
=====================================================================
|    Module Name   : validator.py                                   |
|    Description   : AST-based static analysis tool to validate     |
|                    generated or user-taught code for TAMA.        |
|                                                                   |
|    Author        : Gengai                                         |
|    Created On    : 2025-06-14                                     |
|    Version       : v1.0                                           |
|                                                                   |
|    Purpose       :                                                |
|     - Verify code safety and integrity via AST traversal.         |
|     - Block dangerous calls or unsafe constructs.                 |
|     - Extract metadata about the function (name, args, return).   |
|                                                                   |
|    Usage         :                                                |
|     validator = CodeValidator()                                   |
|     valid, error = validator.validate_code(code)                  |
|     info = validator.extract_function_info(code)                  |
|                                                                   |
|    Future Plans  :                                                |
|     - Add scoring and classification of risk levels.              |
|     - Support multiple function validation per file.              |
=====================================================================
"""
import ast
import builtins
from typing import List, Set

class CodeValidator:
    def __init__(self):
        # Whitelist of safe Python modules
        self.safe_modules = {
            'math', 'random', 'datetime', 'json', 'hashlib', 
            'itertools', 'functools', 'collections', 're'
        }
        
        # Blacklisted dangerous functions
        self.dangerous_funcs = {
            'exec', 'eval', 'compile', '__import__', 'open', 
            'input', 'raw_input', 'file', 'execfile'
        }
        
        # Safe AST node types
        self.safe_nodes = {
            ast.Module, ast.FunctionDef, ast.arguments, ast.arg,
            ast.Return, ast.Expr, ast.Assign, ast.Load, ast.Store,
            ast.BinOp, ast.Call, ast.Name, ast.Constant, ast.List, 
            ast.Tuple, ast.Dict, ast.If, ast.Compare, ast.For, 
            ast.While, ast.Break, ast.Continue, ast.Pass, ast.UnaryOp, 
            ast.Attribute, ast.Subscript, ast.FormattedValue, ast.JoinedStr,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Eq, ast.NotEq,
            ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.And, ast.Or, ast.Not
        }

    def validate_code(self, code: str) -> tuple[bool, str]:
        """
        Comprehensive code validation
        Returns: (is_valid, error_message)
        """
        try:
            tree = ast.parse(code)
            danger_check = self._check_dangerous_nodes(tree)
            if not danger_check[0]:
                return danger_check
            import_check = self._check_imports(tree)
            if not import_check[0]:
                return import_check
            call_check = self._check_function_calls(tree)
            if not call_check[0]:
                return call_check
            func_check = self._check_single_function(tree)
            if not func_check[0]:
                return func_check
            return True, "Code validation passed"
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def _check_dangerous_nodes(self, tree: ast.AST) -> tuple[bool, str]:
        for node in ast.walk(tree):
            if type(node) not in self.safe_nodes:
                return False, f"Dangerous node type: {type(node).__name__}"
        return True, ""

    def _check_imports(self, tree: ast.AST) -> tuple[bool, str]:
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    module_name = alias.name.split('.')[0]
                    if module_name not in self.safe_modules:
                        return False, f"Unsafe import: {module_name}"
        return True, ""

    def _check_function_calls(self, tree: ast.AST) -> tuple[bool, str]:
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.dangerous_funcs:
                        return False, f"Dangerous function call: {node.func.id}"
        return True, ""

    def _check_single_function(self, tree: ast.AST) -> tuple[bool, str]:
        func_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        if len(func_defs) != 1:
            return False, f"Expected 1 function definition, found {len(func_defs)}"
        return True, ""

    def extract_function_info(self, code: str) -> dict:
        tree = ast.parse(code)
        func_def = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
        return {
            'name': func_def.name,
            'args': [arg.arg for arg in func_def.args.args[1:]],  # Skip 'self'
            'has_return': any(isinstance(node, ast.Return) for node in ast.walk(func_def)),
            'line_count': len(code.split('\n'))
        }

# Example usage
if __name__ == "__main__":
    validator = CodeValidator()
    
    # Test safe code
    safe_code = """def greet(self, name):
    return f'Hello, {name}!'"""
    
    # Test dangerous code
    dangerous_code = """def hack(self):
    import os
    os.system('rm -rf /')"""
    
    print("Safe code validation:", validator.validate_code(safe_code))
    print("Dangerous code validation:", validator.validate_code(dangerous_code))
    print("Function info:", validator.extract_function_info(safe_code))
