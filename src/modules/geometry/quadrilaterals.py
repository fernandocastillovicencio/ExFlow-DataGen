"""
Generates quadrilaterals by applying different deformations, shears, and rotations.

This module provides functions to create quadrilaterals, apply horizontal deformations,
shears, and rotations. The generated quadrilaterals are saved as STL and PNG files.

Functions:
- create_square(): Creates a square with side length of 1, centered at (0, 0).
- create_rhombus(): Creates a rhombus by rotating the square 45° around (0, 0).
- generate_quadrilaterals(): Generates and saves all quadrilaterals with deformation, shear, and rotation combinations.

The module ensures that the necessary directories for saving images and STL files exist.
"""

import numpy as np
from modules.geometry.transform_utils import (
    stretch_both_sides,
    rotate_shape,
    shear_horizontal,
)
from modules.geometry.shape_utils import save_as_stl, save_as_png


def create_square():
    """
    Creates a square with side length of 1, centered at (0, 0).

    The vertices are:

    v0 (bottom-left): (-0.5, -0.5, 0)
    v1 (bottom-right): (0.5, -0.5, 0)
    v2 (top-right): (0.5, 0.5, 0)
    v3 (top-left): (-0.5, 0.5, 0)

    The faces are two triangles that form the square:

    f0 (bottom): v0 -> v1 -> v2
    f1 (top): v0 -> v2 -> v3

    Returns:
        tuple: (vertices, faces) - Vertices and faces of the square.
    """
    vertices = np.array(
        [[-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0]]
    )
    faces = [[0, 1, 2], [0, 2, 3]]  # Two triangles that form the square
    return vertices, faces


def create_rhombus():
    """
    Creates a rhombus by rotating the square 45° around (0, 0).

    The rotation is around the origin (0,0) and is counterclockwise.

    Returns:
        tuple: (vertices, faces) - Vertices and faces of the rhombus.
    """
    vertices, faces = create_square()

    # Apply rotation to the square to create a rhombus (losango)
    # The rotation is counterclockwise around the origin (0,0)
    vertices = rotate_shape(vertices, 45)

    return vertices, faces


def generate_quadrilaterals():
    """
    Generate and save quadrilaterals with horizontal shear, stretch, and rotation.

    This function applies horizontal shear, horizontal stretch (both sides), and rotation
    to generate various quadrilaterals and saves them as STL and PNG files.

    The generated quadrilaterals are:

    - Squares and rhombuses with horizontal shear
    - Squares and rhombuses with horizontal stretch (separate factors for left and right sides)
    - Squares and rhombuses with rotation

    The transformations are applied in the order of shear, stretch, and rotation.
    """
    shear_factors = [0.0, 0.1, 0.2, 0.3]  # Shear factors
    deformation_factors = [
        0.75,
        1.0,
        1.5,
    ]  # Deformation factors for both left and right sides
    rotation_angles = [0, 15, 30, 45, 60, 75]  # Rotation angles
    shape_types = [
        "square",
        "rhombus",
    ]  # Two types of initial shapes: square and rhombus

    generated_figures = []  # List to store unique figures

    # Iterate over all combinations of shear, stretch, rotation, and shape type
    for shear_factor in shear_factors:
        for stretch_factor_left in deformation_factors:
            for stretch_factor_right in deformation_factors:
                for rotation_angle in rotation_angles:
                    for shape_type in shape_types:
                        # Create the base shape (square or rhombus)
                        if shape_type == "square":
                            vertices, faces = create_square()
                        elif shape_type == "rhombus":
                            vertices, faces = create_rhombus()

                        # Generate the filename based on the applied transformations
                        filename = f"quadrilateral_Shear{int(shear_factor * 100):03d}_StretchL{int(stretch_factor_left * 100)}_StretchR{int(stretch_factor_right * 100)}_Rot{rotation_angle:03d}"

                        # Apply horizontal shear
                        # The shear is applied before the stretch and rotation
                        vertices = shear_horizontal(vertices, shear_factor)

                        # Apply horizontal stretch (separate factors for left and right)
                        # The stretch is applied after the shear and before the rotation
                        vertices = stretch_both_sides(
                            vertices, stretch_factor_left, stretch_factor_right
                        )

                        # Apply rotation
                        # The rotation is applied after the shear and stretch
                        vertices = rotate_shape(vertices, rotation_angle)

                        # Save the generated shape as both STL and PNG
                        save_as_stl(vertices, faces, filename)
                        save_as_png(vertices, filename)

                        # Add this figure to the list of generated figures
                        generated_figures.append(vertices)
