"""
Handles shape generation and saving for obstacles.

This module provides functions to generate and save various geometric obstacle shapes,
including ellipsoids, semicircles, and triangles. Each shape is saved as both STL and PNG files
in their respective directories.

Functions:
- generate_obstacles(): Orchestrates the generation of ellipsoids, semicircles, and triangles.

The module ensures that the necessary directories for saving images and STL files exist.
"""

# Import functions to generate different geometric shapes
# src/modules/geometry/obstacles.py
# from modules.geometry.ellipsoids import generate_ellipsoids


# from modules.geometry.semicircles import generate_semicircles
# from modules.geometry.quadrilaterals import generate_quadrilaterals
from modules.geometry.combined_circ_tri import generate_combined_circle_triangle


def generate_obstacles():
    """
    Generate and save ellipsoids, semicircles, triangles, and quadrilaterals.

    This function orchestrates the generation of various geometric obstacle shapes,
    ensuring each shape is saved as both STL and PNG files in their respective directories.
    """
    # Generate and save ellipsoids: These are deformed and rotated circles
    # generate_ellipsoids()

    # # Generate and save semicircles: Half circles with deformation and rotation
    # generate_semicircles()

    # # Generate and save triangles: Triangles with different stretch factors and rotations
    # generate_triangles()

    # Generate and save quadrilaterals: Squares with horizontal stretching and rotation
    # generate_quadrilaterals()

    # ---------------------------------------------------------------------------- #
    generate_combined_circle_triangle()


# Execute directly if needed
if __name__ == "__main__":
    # Generate and save obstacles when the script is run directly
    generate_obstacles()
