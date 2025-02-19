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

import numpy as np
from shapely.geometry import Polygon


# -------------------------------------------------------- #
#                     STRETCH ONE SIDE                     #
# -------------------------------------------------------- #
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
    if side not in ["left", "right"]:
        raise ValueError("The 'side' argument must be 'left' or 'right'.")

    # Get the vertices of the geometry
    vertices = np.array([list(coord) + [0] for coord in geometry.exterior.coords])

    # Stretch the specified half
    if side == "left":
        # Stretch vertices with x <= 0
        vertices[vertices[:, 0] <= 0, 0] *= factor
    else:
        # Stretch vertices with x >= 0
        vertices[vertices[:, 0] >= 0, 0] *= factor

    # Return the geometry with the altered vertices
    return Polygon(vertices[:, :2])


# -------------------------------------------------------- #
#                    STRETCH BOTH SIDES                    #
# -------------------------------------------------------- #
def stretch_both_sides(geometry, factor):
    """
    Stretches both sides (left and right) of the geometry with the specified factor.

    Parameters:
        geometry (Polygon): The geometry to be stretched.
        factor (float): The stretching factor to be applied.

    Returns:
        Polygon: The geometry with the altered vertices.
    """
    # Get the vertices of the geometry
    vertices = np.array([list(coord) + [0] for coord in geometry.exterior.coords])

    # Stretch both sides (left and right)
    # The condition vertices[:, 0] <= 0 selects vertices with x <= 0 (left side)
    # and the condition vertices[:, 0] >= 0 selects vertices with x >= 0 (right side)
    vertices[vertices[:, 0] <= 0, 0] *= factor
    vertices[vertices[:, 0] >= 0, 0] *= factor

    # Return the geometry with the altered vertices
    return Polygon(vertices[:, :2])


# -------------------------------------------------------- #
#                         ROTATION                         #
# -------------------------------------------------------- #
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
    if isinstance(geometry, Polygon):
        vertices = np.array(geometry.exterior.coords)
    else:
        vertices = np.array(geometry)

    # Ensure there is at least one valid dimension for multiplication
    if vertices.ndim == 1:
        vertices = vertices.reshape(1, -1)

    # Convert the angle from degrees to radians
    angle_radians = np.radians(angle_degrees)

    # 2D rotation matrix (for rotation in the XY plane)
    rotation_matrix = np.array(
        [
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians), np.cos(angle_radians)],
        ]
    )

    # Applying the rotation
    rotated_vertices = vertices[:, :2] @ rotation_matrix.T  # Matrix multiplication

    # If the input was a Polygon, return a rotated Polygon
    if isinstance(geometry, Polygon):
        return Polygon(rotated_vertices)

    return rotated_vertices


# -------------------------------------------------------- #
