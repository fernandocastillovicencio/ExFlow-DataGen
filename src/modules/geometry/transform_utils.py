# src/modules/geometry/transform_utils.py
"""
Transformation utilities for shape deformation and rotation.
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
    deformed_vertices = vertices.copy()

    # Select the correct side by creating a boolean mask
    if side == "left":
        # Select left side (x < 0)
        mask = deformed_vertices[:, 0] < 0
    elif side == "right":
        # Select right side (x > 0)
        mask = deformed_vertices[:, 0] > 0
    else:
        raise ValueError("Side must be 'left' or 'right'.")

    # Apply scaling only on X-axis
    deformed_vertices[mask, 0] *= deformation_factor

    return deformed_vertices


def stretch_both_sides(vertices, left_factor, right_factor):
    """
    Apply different horizontal deformations to the left and right halves.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        left_factor (float): Stretch/compression factor for left side.
        right_factor (float): Stretch/compression factor for right side.

    Returns:
        np.ndarray: Fully deformed vertices.
    """
    # Deform the left side of the shape
    vertices_left = stretch_one_side(vertices, left_factor, "left")

    # Deform the right side of the shape
    vertices_right = stretch_one_side(vertices_left, right_factor, "right")

    # Return the fully deformed vertices
    return vertices_right


def rotate_shape(vertices, angle_degrees):
    """
    Rotate a shape counterclockwise around (0,0) by a given angle.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        angle_degrees (float): Rotation angle in degrees.

    Returns:
        np.ndarray: Rotated vertices.
    """
    # Convert angle from degrees to radians
    angle_radians = np.radians(angle_degrees)

    # Create the rotation matrix
    rotation_matrix = np.array(
        [
            # cos, -sin, 0
            [np.cos(angle_radians), -np.sin(angle_radians), 0],
            # sin, cos, 0
            [np.sin(angle_radians), np.cos(angle_radians), 0],
            # 0, 0, 1
            [0, 0, 1],
        ]
    )

    # Apply rotation to the vertices
    return vertices @ rotation_matrix.T


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
    # Rotate first semicircle by 180 degrees to create the second semicircle
    rotation_matrix = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
    vertices2 = vertices1 @ rotation_matrix.T  # Apply rotation

    # Offset face indices for the second semicircle
    faces2 = (np.array(faces1) + len(vertices1)).tolist()

    # Merge both halves
    vertices = np.vstack((vertices1, vertices2))
    faces = faces1 + faces2

    return vertices, faces
