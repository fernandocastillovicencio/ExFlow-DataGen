# src/modules/geometry/transform_utils.py
"""
Transformation utilities for shape deformation and rotation.

This module provides functions to apply various transformations to geometric shapes,
including stretching and rotating shapes. The functions are designed to handle both
2D and 3D shapes.

Functions:
- stretch_one_side(vertices, deformation_factor, side): Applies horizontal deformation
  to one half of the shape, either left or right.
- stretch_both_sides(vertices, left_factor, right_factor): Applies different horizontal
  deformations to the left and right halves of the shape.
- rotate_shape(vertices, angle_degrees): Rotates a shape counterclockwise around (0,0)
  by a given angle, handling both 2D and 3D shapes.
- merge_shapes(vertices1, faces1): Merges two semicircles to create a full circle by
  rotating the first semicircle by 180 degrees and combining the vertices and faces.
"""

# ---------------------------------------------------------------------------- #
# Import necessary modules
import numpy as np  # Import NumPy for numerical operations
from shapely.geometry import (
    Polygon,
)  # Import Polygon from Shapely for geometric operations


# -------------------------------------------------------- #
#                     STRETCH ONE SIDE                     #
# -------------------------------------------------------- #
# Define the stretch_one_side function
def stretch_one_side(geometry, side, factor):
    """
    Stretches one half of the geometry with the specified factor.

    Parameters:
        geometry (Polygon): The geometry to be stretched.
        side (str): The side to be stretched, can be 'left' or 'right'.
        factor (float): The stretching factor to be applied.

    Returns:
        Polygon: The geometry with the specified half stretched.

    Raises:
        ValueError: If the 'side' argument is not 'left' or 'right'.
    """
    if side not in ["left", "right"]:  # Check if the side is valid
        raise ValueError(
            "The 'side' argument must be 'left' or 'right'."
        )  # Raise an error if the side is invalid

    # Get the vertices of the geometry
    vertices = np.array(
        [list(coord) + [0] for coord in geometry.exterior.coords]
    )  # Convert geometry to NumPy array

    # Stretch the specified half
    if side == "left":  # Check if the side is 'left'
        # Stretch vertices with x <= 0
        vertices[
            vertices[:, 0] <= 0, 0
        ] *= factor  # Apply stretching factor to the left side
    else:  # If the side is 'right'
        # Stretch vertices with x >= 0
        vertices[
            vertices[:, 0] >= 0, 0
        ] *= factor  # Apply stretching factor to the right side

    # Return the geometry with the altered vertices
    return Polygon(vertices[:, :2])  # Return the stretched geometry as a Polygon


# -------------------------------------------------------- #
#                    STRETCH BOTH SIDES                    #
# -------------------------------------------------------- #
# Define the stretch_both_sides function
def stretch_both_sides(geometry, factor):
    """
    Stretches both sides (left and right) of the geometry with the specified factors.

    Parameters:
        geometry (Polygon): The geometry to be stretched.
        left_factor (float): The stretching factor to be applied to the left side.
        right_factor (float): The stretching factor to be applied to the right side.

    Returns:
        Polygon: The geometry with the altered vertices.
    """
    # Get the vertices of the geometry
    vertices = np.array(
        [list(coord) + [0] for coord in geometry.exterior.coords]
    )  # Convert geometry to NumPy array

    # Stretch both sides (left and right) with different factors
    vertices[
        vertices[:, 0] <= 0, 0
    ] *= factor  # Apply stretching factor to the left side
    vertices[
        vertices[:, 0] >= 0, 0
    ] *= factor  # Apply stretching factor to the right side

    # Return the geometry with the altered vertices
    return Polygon(vertices[:, :2])  # Return the stretched geometry as a Polygon


# -------------------------------------------------------- #
#                         ROTATION                         #
# -------------------------------------------------------- #
# Define the rotate_shape function
def rotate_shape(geometry, angle_degrees):
    """
    Rotates a 2D geometry around its centroid.

    Parameters:
        geometry (Polygon or array-like): The geometry (Shapely Polygon or NumPy array)
            to be rotated.
        angle_degrees (float): The rotation angle in degrees.

    Returns:
        Polygon or array-like: The rotated geometry (Shapely Polygon or NumPy array).
    """
    # If it is a Shapely object, extract the vertices and convert to NumPy array
    if isinstance(geometry, Polygon):  # Check if the geometry is a Polygon
        vertices = np.array(geometry.exterior.coords)  # Convert Polygon to NumPy array
    else:  # If the geometry is not a Polygon
        vertices = np.array(geometry)  # Convert geometry to NumPy array

    # Ensure there is at least one valid dimension for multiplication
    if vertices.ndim == 1:  # Check if the vertices array is 1-dimensional
        vertices = vertices.reshape(1, -1)  # Reshape the array to 2-dimensional

    # Convert the angle from degrees to radians
    angle_radians = np.radians(angle_degrees)  # Convert angle to radians

    # 2D rotation matrix (for rotation in the XY plane)
    rotation_matrix = np.array(
        [
            [
                np.cos(angle_radians),
                -np.sin(angle_radians),
            ],  # First row of the rotation matrix
            [
                np.sin(angle_radians),
                np.cos(angle_radians),
            ],  # Second row of the rotation matrix
        ]
    )

    # Applying the rotation
    rotated_vertices = (
        vertices[:, :2] @ rotation_matrix.T
    )  # Matrix multiplication to rotate vertices

    # If the input was a Polygon, return a rotated Polygon
    if isinstance(geometry, Polygon):  # Check if the input was a Polygon
        return Polygon(rotated_vertices)  # Return the rotated Polygon

    return rotated_vertices  # Return the rotated vertices as a NumPy array


# -------------------------------------------------------- #
