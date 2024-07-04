# run_function.py

import importlib
import argparse

def run_function(module_name, function_name):
    try:
        module = importlib.import_module(module_name)
        func = getattr(module, function_name)
        func()
    except AttributeError:
        print(f"Function '{function_name}' not found in module '{module_name}'")
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found")
    except Exception as e:
        print(f"Error while running the function: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a specific function from a module.')
    parser.add_argument('module', type=str, help='The module name')
    parser.add_argument('function', type=str, help='The function name')

    args = parser.parse_args()

    run_function(args.module, args.function)
