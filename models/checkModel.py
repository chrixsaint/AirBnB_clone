def is_builtin_module(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

# Example usage
module_to_check = "storage"
if is_builtin_module(module_to_check):
    print(f"{module_to_check} is a built-in module.")
else:
    print(f"{module_to_check} is not a built-in module.")
