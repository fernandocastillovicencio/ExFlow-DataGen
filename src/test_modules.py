# src/test_modules.py
"""
Script to test individual geometry generation functions.
"""

import argparse
from modules.geometry.obstacles import generate_and_save_circle

parser = argparse.ArgumentParser(description="Test individual geometry modules")
parser.add_argument(
    "--test",
    type=str,
    required=True,
    help="Specify the shape to test (circle, semicircle, etc.)",
)

args = parser.parse_args()

if args.test == "circle":
    generate_and_save_circle()
    print("Test complete: Circle generated.")
else:
    print("Invalid test option. Available: circle.")
