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

import numpy as np


def stretch_one_side(vertices, deformation_factor, side):
    """
    Apply horizontal deformation to one half of the shape.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        deformation_factor (float): Stretch/compression factor.
        side (str): "left" or "right" to apply deformation correctly.

    Returns:
        np.ndarray: Deformed vertices.
    """
    # Create a copy of the vertices to apply transformations
    deformed_vertices = vertices.copy()

    # Determine which side to deform based on the 'side' parameter
    if side == "left":
        # Create a mask for the left side (x < 0)
        mask = deformed_vertices[:, 0] < 0
    elif side == "right":
        # Create a mask for the right side (x > 0)
        mask = deformed_vertices[:, 0] > 0
    else:
        # If the side is invalid, raise an error
        raise ValueError("Side must be 'left' or 'right'.")

    # Apply the deformation factor to the selected side on the X-axis
    deformed_vertices[mask, 0] *= deformation_factor

    # Return the deformed vertices
    return deformed_vertices


def stretch_both_sides(vertices, left_factor, right_factor):
    """
    Apply different horizontal deformations to the left and right halves.

    This function takes the input vertices and applies different stretch or compression
    factors to the left and right halves of the shape. The resulting vertices represent
    the fully deformed shape.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        left_factor (float): Stretch/compression factor for left side (x < 0).
        right_factor (float): Stretch/compression factor for right side (x > 0).

    Returns:
        np.ndarray: Fully deformed vertices (N,3).
    """
    # Deform the left side of the shape (x < 0)
    vertices_left = stretch_one_side(vertices, left_factor, "left")

    # Deform the right side of the shape (x > 0)
    vertices_right = stretch_one_side(vertices_left, right_factor, "right")

    # Return the fully deformed vertices
    return vertices_right


def shear_horizontal(vertices, shear_factor):
    """
    Apply horizontal shear transformation to the shape.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        shear_factor (float): Shear factor to control the magnitude of shearing.

    Returns:
        np.ndarray: Sheared vertices.
    """
    # Apply shear transformation
    sheared_vertices = vertices.copy()

    # Apply shear to each vertex
    sheared_vertices[:, 0] += (
        shear_factor * sheared_vertices[:, 1]
    )  # shear factor applied to x

    return sheared_vertices


def rotate_shape(vertices, angle_degrees):
    """
    Rotate a shape counterclockwise around (0,0) by a given angle.

    This function handles both 2D and 3D vertices. The rotation is done in the XY plane
    for 3D shapes, effectively rotating the shape around the Z-axis.

    Parameters:
        vertices (np.ndarray): Shape vertices (N, 2 or 3), with optional z=0 for 2D shapes.
        angle_degrees (float): Rotation angle in degrees.

    Returns:
        np.ndarray: Rotated vertices (N, 2 or 3).
    """
    # Convert angle from degrees to radians
    angle_radians = np.radians(angle_degrees)

    # Check if the shape is 2D or 3D (check if z exists in the vertices)
    if vertices.shape[1] == 2:  # 2D
        # Rotation matrix for 2D rotation
        rotation_matrix = np.array(
            [
                [np.cos(angle_radians), -np.sin(angle_radians)],
                [np.sin(angle_radians), np.cos(angle_radians)],
            ]
        )
        # Apply rotation to x and y, z remains unchanged (implicitly)
        rotated_vertices = vertices @ rotation_matrix.T
        return rotated_vertices

    elif vertices.shape[1] == 3:  # 3D
        # Rotation matrix for 3D rotation in the XY plane
        rotation_matrix = np.array(
            [
                [np.cos(angle_radians), -np.sin(angle_radians), 0],
                [np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1],
            ]
        )
        # Apply rotation to x, y and z (rotation in the XY plane)
        rotated_vertices = vertices @ rotation_matrix.T
        return rotated_vertices

    else:
        raise ValueError("Vertices must have 2 or 3 columns (2D or 3D shapes).")


def merge_shapes(vertices1, faces1):
    """
    Merge two semicircles to create a full circle.

    This function takes the vertices and faces of one semicircle, creates a second
    semicircle by rotating the first one by 180 degrees, and then merges both to
    create a full circle.

    Parameters:
        vertices1 (np.ndarray): Vertices of the first semicircle (N,3).
        faces1 (list): Faces of the first semicircle.

    Returns:
        tuple: (vertices, faces) - Full merged shape.
    """
    # Create a rotation matrix to rotate the first semicircle by 180 degrees.
    # This is equivalent to flipping the x and y axes.
    rotation_matrix = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])

    # Apply the rotation matrix to the vertices of the first semicircle to create
    # the second semicircle.
    vertices2 = vertices1 @ rotation_matrix.T

    # Offset the face indices of the second semicircle by the length of the first
    # semicircle. This is because the faces of the second semicircle are computed
    # relative to the vertices of the first semicircle.
    faces2 = (np.array(faces1) + len(vertices1)).tolist()

    # Merge the vertices and faces of both semicircles to create the full circle.
    vertices = np.vstack((vertices1, vertices2))
    faces = faces1 + faces2

    return vertices, faces
