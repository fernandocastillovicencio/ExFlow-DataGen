"""
Generates semicircles by applying different deformations and rotations.

This module provides functions to create semicircles, apply horizontal deformations,
and rotate the shapes. The generated semicircles are saved as STL and PNG files.

Functions:
- create_semicircle(): Computes the vertices and faces of a semicircle.
- generate_semicircles(): Generates and saves all semicircles with deformation and rotation combinations.

The module ensures that the necessary directories for saving images and STL files exist.
"""

import numpy as np
from modules.geometry.transform_utils import stretch_one_side
from modules.geometry.shape_utils import save_as_stl, save_as_png


def create_semicircle():
    """
    Compute the vertices and faces of a semicircle.

    The semicircle is centered at (0,0), has a radius of 1, and its curved edge passes
    through the points (0,1), (-1,0), and (0,-1). The straight edge of the semicircle
    is from (0,1) to (0,-1).

    Returns:
        tuple: (vertices, faces)

    Notes:
        - The semicircle is centered at (0,0)
        - The radius of the semicircle is 1
        - The curved edge passes through the points (0,1), (-1,0), and (0,-1)
        - The straight edge is from (0,1) to (0,-1)
    """
    radius_m = 1.0
    num_points = 50  # Number of points for smooth curvature

    # Compute the points for the curved edge
    theta = np.linspace(np.pi / 2, 3 * np.pi / 2, num=num_points)
    x = radius_m * np.cos(theta)
    y = radius_m * np.sin(theta)
    z = np.zeros_like(x)

    # Compute the points for the straight edge
    x_straight = np.array([0, 0])
    y_straight = np.array([1, -1])
    z_straight = np.zeros_like(x_straight)

    # Create the vertices
    vertices = np.column_stack(
        (
            np.concatenate([x, x_straight]),
            np.concatenate([y, y_straight]),
            np.concatenate([z, z_straight]),
        )
    )

    # Create the faces (triangular faces for the shape)
    faces = [[i, i + 1, len(vertices) - 1] for i in range(len(vertices) - 2)]
    faces.append([len(vertices) - 2, 0, len(vertices) - 1])

    return vertices, faces


def generate_semicircles():
    """
    Generate and save all semicircles as STL and PNG files.

    This function generates semicircles with various transformations (e.g., deformation and rotation)
    and saves them as both STL files and PNG images.

    The generated semicircles have the following properties:
    - Centered at (0,0)
    - Radius = 1
    - Curved edge through (0,1), (-1,0), (0,-1)
    - Straight edge from (0,1) to (0,-1)

    The transformations applied are:
    - Deformation (stretch or compress the shape horizontally) with factors
      0.75, 1.0, 1.5, 2.0
    - Rotation with angles 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180

    The filename for each semicircle is constructed as:
    semicircle_Def<deformation_factor * 100>_Rot<rotation_angle>

    STL files are saved in geometries/obstacles/stl/ and PNG images are saved in
    geometries/obstacles/images/.
    """
    # Define the deformation factors and rotation angles for the semicircles
    DEFORMATION_FACTORS = [0.75, 1.0, 1.5, 2.0]

    ROTATION_ANGLES = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]

    # Iterate through each transformation to generate and save semicircles
    for deformation_factor in DEFORMATION_FACTORS:
        for rotation_angle in ROTATION_ANGLES:
            # Generate the semicircle
            vertices, faces = create_semicircle()

            # Apply deformation (stretch or compress the shape horizontally)
            # Example: stretch left side
            vertices = stretch_one_side(vertices, deformation_factor, "left")

            # Apply rotation
            vertices = rotate_shape(vertices, rotation_angle)

            # Construct a filename based on the transformations
            filename = f"semicircle_Def{int(deformation_factor * 100):03d}_Rot{rotation_angle:03d}"

            # Save the semicircle as STL and PNG
            save_as_stl(vertices, faces, filename)
            save_as_png(vertices, filename)
