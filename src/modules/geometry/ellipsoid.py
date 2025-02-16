# src/modules/geometry/ellipsoid.py
"""
Generates an ellipsoid by applying different deformations to each half.
"""

import numpy as np
from modules.geometry.semicircle import generate_semicircle
from modules.geometry.transform_utils import deform_ellipsoid
from modules.geometry.shape_utils import save_as_stl, save_as_png

# Deformation factors for left and right halves
DEFORMATION_FACTORS = [0.75, 1.0, 1.5, 2.5]


def generate_ellipsoid(left_factor, right_factor):
    """
    Generate an ellipsoid by deforming a circle using different horizontal factors.

    Parameters:
        left_factor (float): Stretch/compression factor for left side.
        right_factor (float): Stretch/compression factor for right side.

    Returns:
        tuple: (vertices, faces) - Computed points and faces for the ellipsoid.
    """
    # Generate two semicircles
    vertices1, faces1 = generate_semicircle()

    # Rotate first semicircle by 180 degrees to create the second semicircle
    rotation_matrix = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
    vertices2 = vertices1 @ rotation_matrix.T  # Apply rotation

    # Offset face indices for the second semicircle
    faces2 = (np.array(faces1) + len(vertices1)).tolist()

    # Merge both halves
    vertices = np.vstack((vertices1, vertices2))
    faces = faces1 + faces2

    # Apply deformation
    vertices = deform_ellipsoid(vertices, left_factor, right_factor)

    return vertices, faces


def generate_and_save_all_ellipsoids():
    """
    Generate and save all possible ellipsoids with deformation combinations.
    """
    for left_factor in DEFORMATION_FACTORS:
        for right_factor in DEFORMATION_FACTORS:
            filename = f"ellipsoid_Ldef{int(left_factor * 100):03d}_Rdef{int(right_factor * 100):03d}"
            vertices, faces = generate_ellipsoid(left_factor, right_factor)
            save_as_stl(vertices, faces, filename)
            save_as_png(vertices, filename)


# Execute directly if needed
if __name__ == "__main__":
    generate_and_save_all_ellipsoids()
