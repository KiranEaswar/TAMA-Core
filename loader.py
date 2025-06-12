# loader.py
import types
from validator import CodeValidator
from storage import PatchStorage, StorageError

class PatchLoader:
    def __init__(self, storage: PatchStorage):
        self.storage = storage
        self.validator = CodeValidator()

    def load_patch(self, obj, func_hash: str) -> bool:
        """
        Loads a patch from storage and attaches it to the given object.
        Returns True if successful, False otherwise.
        """
        patch = self.storage.get_patch(func_hash)
        if not patch:
            print(f"No patch found for hash: {func_hash}")
            return False

        code = patch['code']
        
        # Use dedicated validator
        is_valid, error_msg = self.validator.validate_code(code)
        if not is_valid:
            print(f"Code validation failed: {error_msg}")
            return False

        # Extract function name using validator's metadata
        try:
            func_info = self.validator.extract_function_info(code)
            func_name = func_info['name']
        except Exception as e:
            print(f"Could not extract function name: {e}")
            return False

        # Prepare namespace and exec
        namespace = {}
        try:
            exec(code, namespace)
            func = namespace[func_name]
            setattr(obj, func_name, types.MethodType(func, obj))
            print(f"Loaded '{func_name}' onto {obj.__class__.__name__}")
            return True
        except Exception as e:
            print(f"Error loading patch: {e}")
            return False

# Example usage
if __name__ == "__main__":
    from storage import PatchStorage

    class MyBot:
        pass

    storage = PatchStorage()
    loader = PatchLoader(storage)

    # Store a sample patch if not already present
    code = "def greet(self):\n    return f'Hello, {self.__class__.__name__}!'"
    hash_ = storage.store_patch(code)
    bot = MyBot()

    # Load the patch and test
    if loader.load_patch(bot, hash_):
        print(bot.greet())  # Output: "Hello, MyBot!"
