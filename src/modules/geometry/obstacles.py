# src/modules/geometry/obstacles.py
"""
Handles shape generation and saving for obstacles.
"""

from modules.geometry.semicircle import generate_semicircle
from modules.geometry.shape_utils import save_as_stl, save_as_png


def generate_and_save_semicircle():
    """
    Generate a semicircle and save it as STL and PNG.
    """
    vertices, faces = generate_semicircle()
    save_as_stl(vertices, faces, "semicircle")
    save_as_png(vertices, "semicircle")


# Execute directly if needed
if __name__ == "__main__":
    generate_and_save_semicircle()
