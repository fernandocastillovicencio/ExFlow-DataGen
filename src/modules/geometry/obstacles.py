# src/modules/geometry/obstacles.py
"""
Handles shape generation and saving for obstacles.
"""

from modules.geometry.ellipsoid import generate_and_save_all_ellipsoids
from modules.geometry.shape_utils import save_as_stl, save_as_png
from modules.geometry.semicircle import generate_semicircle
from modules.geometry.ellipsoid import generate_ellipsoid


def generate_and_save_ellipsoids():
    """
    Generate all ellipsoids with different deformations and save as STL/PNG.
    """
    generate_and_save_all_ellipsoids()


# Execute directly if needed
if __name__ == "__main__":
    generate_and_save_ellipsoids()
