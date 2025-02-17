"""
Generates triangles by applying different deformations and rotations.

This module provides functions to create triangles, apply horizontal deformations,
and rotate the shapes. The generated triangles are saved as STL and PNG files.

Functions:
- create_triangle(): Computes the vertices and faces of an equilateral triangle.
- generate_triangles(): Generates and saves all triangles with deformation and rotation combinations.

The module ensures that the necessary directories for saving images and STL files exist.
"""

# src/modules/geometry/triangles.py
import numpy as np
from modules.geometry.transform_utils import rotate_shape, stretch_both_sides
from modules.geometry.shape_utils import (
    save_as_stl,
    save_as_png,
)  # Remova o check_redundancy aqui


def create_triangle():
    """
    Compute the vertices and faces of an equilateral triangle inscribed in a circle with radius 1m.

    The side length of the triangle is 2.0 meters, and the triangle's base is aligned horizontally.

    The triangle is centered at (0, 0), with the base (bottom edge) being horizontal.

    Returns:
        tuple: (vertices, faces)
    """
    radius = 1.0  # Radius of the circle

    # Vértice superior (no topo do círculo)
    V1 = (0, radius, 0)  # Top vertex

    # Vértices inferiores (calculados com base no ângulo de 120° entre eles)
    V2 = (
        np.cos(np.radians(120)) * radius,
        np.sin(np.radians(120)) * radius,
        0,
    )  # Bottom-left vertex
    V3 = (
        np.cos(np.radians(240)) * radius,
        np.sin(np.radians(240)) * radius,
        0,
    )  # Bottom-right vertex

    vertices = np.array([V1, V2, V3])
    faces = [[0, 1, 2]]  # Single face formed by the three vertices
    return vertices, faces


def generate_triangles():
    """
    Generate and save all triangles with various transformations (stretch and rotation).

    This function generates triangles by applying different stretch factors (horizontal deformation) to the left and right halves,
    and then rotates each transformed triangle. Each transformed triangle is saved as both an STL and a PNG file.

    Transformation parameters:
    - Deformation factors: 0.75, 1.0, 1.5, 2.0
    - Rotation angles: 0, 15, 30, 45, 60, 90, 120, 135, 150 degrees
    """
    DEFORMATION_FACTORS = [
        0.75,
        1.0,
        1.5,
        2.0,
    ]  # Deformation factors for each half of the triangle
    ROTATION_ANGLES = [
        0,
        15,
        30,
        45,
        60,
        90,
        120,
        135,
        150,
    ]  # Rotation angles for the triangles

    generated_figures = []  # List to store unique figures

    # Iterate over each combination of deformation and rotation
    for left_factor in DEFORMATION_FACTORS:
        for right_factor in DEFORMATION_FACTORS:
            for rotation_angle in ROTATION_ANGLES:
                # Construct the filename based on the applied transformations
                filename = f"triangle_Ldef{int(left_factor * 100)}_Rdef{int(right_factor * 100)}_Rot{rotation_angle}"

                # Generate the base equilateral triangle
                vertices, faces = create_triangle()

                # Apply deformation to both sides of the triangle
                vertices = stretch_both_sides(vertices, left_factor, right_factor)

                # Apply rotation
                vertices = rotate_shape(vertices, rotation_angle)

                # Save the generated shape as both STL and PNG
                save_as_stl(vertices, faces, filename)
                save_as_png(vertices, filename)

                # Add this figure to the list of generated figures
                generated_figures.append(vertices)


# Execute directly if needed
if __name__ == "__main__":
    generate_triangles()
