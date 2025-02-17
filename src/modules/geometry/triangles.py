"""
Generates triangles by applying different deformations and rotations.

This module provides functions to create triangles, apply horizontal deformations,
and rotate the shapes. The generated triangles are saved as STL and PNG files.

Functions:
- create_triangle(): Computes the vertices and faces of an equilateral triangle.
- generate_triangles(): Generates and saves all triangles with deformation and rotation combinations.

The module ensures that the necessary directories for saving images and STL files exist.
"""

import numpy as np
from modules.geometry.transform_utils import (
    rotate_shape,
    stretch_both_sides,
)
from modules.geometry.shape_utils import save_as_stl, save_as_png


def create_triangle():
    """
    Compute the vertices and faces of an equilateral triangle with the base pointing downwards.

    The side length of the triangle is set to 2.0, which ensures the height is 1 meter for a triangle with unit radius.

    The triangle is centered at (0,0) and its horizontal base points down.

    Returns:
        tuple: (vertices, faces)
    """
    # Side length of the equilateral triangle
    side_length = 2.0  # side length to ensure the height is 1 meter
    height = np.sqrt(3) / 2 * side_length  # Height of an equilateral triangle

    # Define the three vertices of the triangle (with base pointing down)
    # V1: Top vertex (now below the center)
    # V2: Bottom-left vertex
    # V3: Bottom-right vertex
    V1 = (0, -height, 0)
    V2 = (-side_length / 2, 0, 0)
    V3 = (side_length / 2, 0, 0)

    vertices = np.array([V1, V2, V3])

    # Define the face of the triangle
    # The single face formed by the three vertices
    faces = [[0, 1, 2]]

    return vertices, faces


def generate_triangles():
    """
    Generate and save all triangles with various transformations (stretch and rotation).

    This function generates triangles by applying different stretch factors (horizontal deformation) to the left and right halves,
    and then rotates each transformed triangle. Each transformed triangle is saved as both an STL and a PNG file.

    The deformation factors determine how much the triangle is stretched or compressed, while the rotation angles determine
    the rotation applied to the triangle.

    Transformation parameters:
    - Deformation factors: 0.75, 1.0, 1.5, 2.0
    - Rotation angles: 0, 15, 30, 45, 60, 90, 120, 135, 150 degrees

    Files are saved in predefined directories for STL and PNG files.
    """
    # Define the deformation factors for each half of the triangle
    DEFORMATION_FACTORS = [0.75, 1.0, 1.5, 2.0]
    # Define the rotation angles for the triangles
    ROTATION_ANGLES = [0, 15, 30, 45, 60, 90, 120, 135, 150]

    # Iterate over each combination of deformation and rotation
    for left_factor in DEFORMATION_FACTORS:
        for right_factor in DEFORMATION_FACTORS:
            for rotation_angle in ROTATION_ANGLES:
                # Construct the filename based on the applied transformations
                filename = f"triangle_Ldef{int(left_factor * 100):03d}_Rdef{int(right_factor * 100):03d}_Rot{rotation_angle:03d}"

                # Generate the base equilateral triangle
                vertices, faces = create_triangle()

                # Apply deformation to both sides of the triangle
                vertices = stretch_both_sides(vertices, left_factor, right_factor)

                # Rotate the deformed triangle by the specified angle
                vertices = rotate_shape(vertices, rotation_angle)

                # Save the transformed triangle as an STL file
                save_as_stl(vertices, faces, filename)
                # Save the transformed triangle as a PNG image
                save_as_png(vertices, filename)


# Execute directly if needed
if __name__ == "__main__":
    generate_triangles()
