# src/modules/geometry/rectangle.py
import numpy as np
from modules.geometry.transform_utils import (
    stretch_one_side,
    rotate_shape,
    shear_horizontal,
)
from modules.geometry.shape_utils import save_as_stl, save_as_png


def create_square():
    """
    Creates a square with side length of 1, centered at (0, 0).

    Returns:
        tuple: (vertices, faces) - Vertices and faces of the square.
    """
    # Vertices of the square centered at (0,0) with side length 1
    vertices = np.array(
        [[-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0]]
    )
    faces = [[0, 1, 2], [0, 2, 3]]  # Two triangles that form the square
    return vertices, faces


def generate_quadrilaterals():
    """
    Generate and save quadrilaterals with horizontal shear, stretch, and rotation.

    This function applies horizontal shear, horizontal stretch (both sides), and rotation
    to generate various quadrilaterals and saves them as STL and PNG files.
    """
    shear_factors = [0.0, 0.2, 0.4]  # Shear factors
    deformation_factors = [
        0.75,
        1.0,
        1.5,
        2.0,
    ]  # Deformation factors for both left and right sides
    rotation_angles = [0, 15, 30, 45, 60, 75]  # Rotation angles

    # Iterate over all combinations of shear, stretch, and rotation
    for shear_factor in shear_factors:
        for stretch_factor_left in deformation_factors:
            for stretch_factor_right in deformation_factors:
                for rotation_angle in rotation_angles:
                    # Create the base square
                    vertices, faces = create_square()

                    # Apply horizontal shear
                    vertices = shear_horizontal(vertices, shear_factor)

                    # Apply horizontal stretch (separate factors for left and right)
                    vertices = stretch_one_side(vertices, stretch_factor_left, "left")
                    vertices = stretch_one_side(vertices, stretch_factor_right, "right")

                    # Apply rotation
                    vertices = rotate_shape(vertices, rotation_angle)

                    # Generate a unique filename for each combination
                    filename = f"quadrilateral_Shear{int(shear_factor * 100):03d}_StretchL{int(stretch_factor_left * 100)}_StretchR{int(stretch_factor_right * 100)}_Rot{rotation_angle:03d}"

                    # Save the generated shape as both STL and PNG
                    save_as_stl(vertices, faces, filename)
                    save_as_png(vertices, filename)
