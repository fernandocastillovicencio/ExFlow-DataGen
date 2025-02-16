# src/modules/geometry/ellipsoid.py
"""
Generates an ellipsoid by applying different deformations and rotations.
"""

import numpy as np
from modules.geometry.semicircle import generate_semicircle
from modules.geometry.transform_utils import deform_ellipsoid, rotate_shape
from modules.geometry.shape_utils import save_as_stl, save_as_png

# Deformation factors for left and right halves
DEFORMATION_FACTORS = [0.75, 1.0, 1.5, 2.5]
# Rotation angles in degrees (excluding mirrored redundancies)
ROTATION_ANGLES = [0, 15, 30, 45, 60, 75]


def generate_ellipsoid(left_factor, right_factor, rotation_angle):
    """
    Generate an ellipsoid by deforming and rotating a circle.

    Parameters:
        left_factor (float): Stretch/compression factor for left side.
        right_factor (float): Stretch/compression factor for right side.
        rotation_angle (float): Rotation angle in degrees.

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

    # Apply deformation (sorted to prevent duplicate mirrored shapes)
    left_factor, right_factor = sorted([left_factor, right_factor])
    vertices = deform_ellipsoid(vertices, left_factor, right_factor)

    # Apply rotation (only for non-circle cases)
    if (left_factor, right_factor) != (1.0, 1.0):  # Keep circle without rotation
        vertices = rotate_shape(vertices, rotation_angle)

    return vertices, faces


def generate_and_save_all_ellipsoids():
    """
    Generate and save all possible ellipsoids with deformation and rotation combinations.
    """
    # Generate and save the single circle with correct naming convention
    filename = "ellipsoid_Ldef100_Rdef100_Rot000"
    vertices, faces = generate_ellipsoid(1.0, 1.0, 0)
    save_as_stl(vertices, faces, filename)
    save_as_png(vertices, filename)

    # Generate ellipsoids with deformation and rotation
    for left_factor in DEFORMATION_FACTORS:
        for right_factor in DEFORMATION_FACTORS:
            # Skip if it's a circle (1.0, 1.0) and avoid mirrored cases
            if (left_factor, right_factor) == (1.0, 1.0):
                continue

            for rotation_angle in ROTATION_ANGLES:
                filename = (
                    f"ellipsoid_Ldef{int(left_factor * 100):03d}_"
                    f"Rdef{int(right_factor * 100):03d}_"
                    f"Rot{int(rotation_angle):03d}"
                )
                vertices, faces = generate_ellipsoid(
                    left_factor, right_factor, rotation_angle
                )
                save_as_stl(vertices, faces, filename)
                save_as_png(vertices, filename)


# Execute directly if needed
if __name__ == "__main__":
    generate_and_save_all_ellipsoids()
