# src/modules/geometry/obstacles.py
"""
Handles shape generation and saving for obstacles.
"""

from modules.geometry.ellipsoid import generate_ellipsoids


def generate_and_save_ellipsoids():
    """
    Generate and save all ellipsoids with different deformations as STL and PNG files.

    This function is a convenience wrapper around generate_ellipsoids() to save all
    generated ellipsoids to file.
    """
    generate_ellipsoids()


# Execute directly if needed
if __name__ == "__main__":
    generate_ellipsoids()
