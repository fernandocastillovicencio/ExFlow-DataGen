# src/modules/geometry/obstacles.py
"""
Handles shape generation and saving for obstacles.
"""

import numpy as np
from modules.geometry.semicircle import generate_semicircle
from modules.geometry.shape_utils import save_as_stl, save_as_png


def generate_circle():
    """
    Generate a full circle using two semicircles.

    Steps:
    1. Create the first semicircle.
    2. Rotate the second semicircle by 180 degrees around (0,0).
    3. Merge both semicircles into a single shape.

    Returns:
        tuple: (vertices, faces) - Computed points and faces for the full circle.
    """
    # Generate the first semicircle
    vertices1, faces1 = generate_semicircle()

    # Rotate the first semicircle 180 degrees to create the second semicircle
    rotation_matrix = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]]
    )  # 180-degree rotation
    vertices2 = vertices1 @ rotation_matrix.T  # Apply rotation to all vertices

    # Offset face indices for the second semicircle
    faces2 = (np.array(faces1) + len(vertices1)).tolist()

    # Merge vertices and faces
    vertices = np.vstack((vertices1, vertices2))
    faces = faces1 + faces2

    return vertices, faces


def generate_and_save_circle():
    """
    Generate a circle and save it as STL and PNG.
    """
    vertices, faces = generate_circle()
    save_as_stl(vertices, faces, "circle")
    save_as_png(vertices, "circle")


# Execute directly if needed
if __name__ == "__main__":
    generate_and_save_circle()
