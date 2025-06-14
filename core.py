# core.py
"""
=====================================================================
|    Module Name   : core.py                                        |
|    Description   : Main orchestrator for TAMA. Coordinates intent |
|                    parsing, code generation, validation, loading. |
|                                                                   |
|    Author        : Gengai                                         |
|    Created On    : 2025-06-14                                     |
|    Version       : v1.0                                           |
|                                                                   |
|    Purpose       :                                                |
|     - Takes natural language and turns it into functional code.   |
|     - Stores patches, attaches them, and executes on the fly.     |
|     - Represents TAMA's brain in execution context.               |
|                                                                   |
|    Usage         :                                                |
|     bot = DynamicBot()                                            |
|     bot.learn_and_execute("add two numbers", 1, 2)                |
|                                                                   |
|    Future Plans  :                                                |
|     - Add intent retry strategies.                                |
|     - Integrate mutation, embedding matcher, memory introspection.|
=====================================================================
"""
from storage import PatchStorage
from loader import PatchLoader
from validator import CodeValidator
from nlp import IntentParser
from generator import CodeGenerator


class DynamicBot:
    def __init__(self):
        self.storage = PatchStorage()
        self.validator = CodeValidator()
        self.loader = PatchLoader(self.storage)
        self.intent_parser = IntentParser()
        self.code_generator = CodeGenerator()
        
    def learn_and_execute(self, instruction: str, *args, **kwargs):
        
        # 1. Parse intent
        spec = self.intent_parser.parse(instruction)
        print(f"[Intent] Parsed spec: {spec}")

        # 2. Generate code
        code = self.code_generator.generate(spec)
        print(f"[Generator] Generated code:\n{code}")

        # 3. Validate code
        is_valid, error_msg = self.validator.validate_code(code)
        if not is_valid:
            print(self.personality.react("error"))
            print(f"[Validator] Code rejected: {error_msg}")
            return None

        # 4. Store patch
        func_hash = self.storage.store_patch(code)
        print(f"[Storage] Patch stored with hash: {func_hash}")

        # 5. Load patch
        loaded = self.loader.load_patch(self, func_hash)
        if not loaded:
            print("[Loader] Failed to load patch.")
            return None

        # 6. Call the new function
        func_name = spec['name']
        func = getattr(self, func_name, None)
        if func:
            print(f"[Bot] Executing '{func_name}' with args {args}")
            return func(*args, **kwargs)
        else:
            print(f"[Bot] Function '{func_name}' not found after loading.")
            return None

# Example usage
if __name__ == "__main__":
    bot = DynamicBot()
    result = bot.learn_and_execute("Write a function to multiply two numbers", 3, 5)
    print("Result:", result)
    result = bot.learn_and_execute("Create a function to sort a list", [4, 2, 1])
    print("Result:", result)
    result = bot.learn_and_execute("Divide two numbers",16,4)
    print("Result:", result)
