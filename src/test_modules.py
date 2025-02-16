# src/test_modules.py
"""
Script to test individual geometry generation functions.
"""

import argparse

# Dictionary of available shape test functions
TEST_FUNCTIONS = {}

try:
    from modules.geometry.obstacles import generate_and_save_ellipsoids

    TEST_FUNCTIONS["ellipsoid"] = generate_and_save_ellipsoids
except ImportError as e:
    print(f"Warning: Could not import 'generate_and_save_ellipsoids'. Error: {e}")

parser = argparse.ArgumentParser(description="Test individual geometry modules")
parser.add_argument(
    "--test",
    type=str,
    required=True,
    help="Specify the shape to test (ellipsoid, etc.)",
)

args = parser.parse_args()

# Check if the requested shape test exists
if args.test in TEST_FUNCTIONS:
    TEST_FUNCTIONS[args.test]()  # Call the corresponding function
    print(f"Test complete: {args.test} generated.")
else:
    print("Invalid test option. Available:", ", ".join(TEST_FUNCTIONS.keys()))
