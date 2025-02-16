"""
Script to test individual geometry generation functions.

This script allows the user to test the generation of different geometric shapes
by specifying the shape type as a command-line argument. The available shapes
include ellipsoids, semicircles, and triangles. The script dynamically imports
the necessary functions and executes them based on the user's input.

Usage:
    python src/test_modules.py --test <shape>

Available shapes:
    - ellipsoid
    - semicircle
    - triangle

The script prints a success message upon successful generation of the specified shape.
"""

import argparse

# Dictionary to store available shape test functions
# This dictionary will be populated with functions to generate different shapes
TEST_FUNCTIONS = {}

try:
    # Attempt to import the function to generate ellipsoids
    from modules.geometry.ellipsoids import generate_ellipsoids

    # Add the ellipsoid generation function to the dictionary
    TEST_FUNCTIONS["ellipsoid"] = generate_ellipsoids
except ImportError as e:
    # If the import fails, print a warning message with the error
    print(f"Warning: Could not import 'generate_and_save_all_ellipsoids'. Error: {e}")

try:
    # Attempt to import the function to generate semicircles
    from modules.geometry.semicircles import generate_semicircles

    # Add the semicircle generation function to the dictionary
    TEST_FUNCTIONS["semicircle"] = generate_semicircles
except ImportError as e:
    # If the import fails, print a warning message with the error
    print(f"Warning: Could not import 'generate_and_save_semicircles'. Error: {e}")

try:
    # Attempt to import the function to generate triangles
    from modules.geometry.triangles import generate_triangles

    # Add the triangles generation function to the dictionary
    TEST_FUNCTIONS["triangle"] = generate_triangles
except ImportError as e:
    # If the import fails, print a warning message with the error
    print(f"Warning: Could not import 'generate_and_save_triangles'. Error: {e}")

# Create an ArgumentParser to handle command-line arguments
parser = argparse.ArgumentParser(description="Test individual geometry modules")

# Add a required argument to specify the shape to test
parser.add_argument(
    "--test",
    type=str,
    required=True,
    help="Specify the shape to test (ellipsoid, semicircle, triangle, etc.)",
)

# Parse the command-line arguments
args = parser.parse_args()

# Check if the requested shape test exists in the dictionary
if args.test in TEST_FUNCTIONS:
    # If the shape test exists, call the corresponding function
    TEST_FUNCTIONS[args.test]()
    # Print a success message with the shape that was generated
    print(f"Test complete: {args.test} generated.")
else:
    # If the shape test does not exist, print an error message with available options
    print("Invalid test option. Available:", ", ".join(TEST_FUNCTIONS.keys()))
