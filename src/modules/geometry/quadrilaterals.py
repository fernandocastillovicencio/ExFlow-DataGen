# src/modules/geometry/rectangle.py
import numpy as np
from modules.geometry.transform_utils import stretch_both_sides, rotate_shape
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
    Generate and save quadrilaterals with horizontal stretch and rotation.

    This function applies various stretch factors (0.75, 1.0, 1.5, 2.0) to the square
    and rotates the result by 0°, 15°, 30°, 45°, 60°, and 75° angles.
    Each shape is saved as both STL and PNG files.
    """
    # Define stretch factors and rotation angles
    stretch_factors = [0.75, 1.0, 1.5, 2.0]
    rotation_angles = [0, 15, 30, 45, 60, 75]

    # Generate and save quadrilaterals for each combination of stretch factor and rotation angle
    for stretch_factor in stretch_factors:
        for rotation_angle in rotation_angles:
            # Create the base square
            vertices, faces = create_square()

            # Apply horizontal stretch to the square
            vertices = stretch_both_sides(vertices, stretch_factor, stretch_factor)

            # Apply rotation to the deformed square
            vertices = rotate_shape(vertices, rotation_angle)

            # Generate filename based on stretch factor and rotation angle
            filename = f"rectangle_Stretch{int(stretch_factor * 100):03d}_Rot{rotation_angle:03d}"

            # Save the generated shape as both STL and PNG
            save_as_stl(vertices, faces, filename)
            save_as_png(vertices, filename)
