# src/modules/geometry/transform_utils.py
"""
Transformation utilities for shape deformation.
"""

import numpy as np


def deform_half(vertices, deformation_factor, side):
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

    if side == "left":
        mask = deformed_vertices[:, 0] < 0  # Select left side (x < 0)
    elif side == "right":
        mask = deformed_vertices[:, 0] > 0  # Select right side (x > 0)
    else:
        raise ValueError("Side must be 'left' or 'right'.")

    deformed_vertices[mask, 0] *= deformation_factor  # Apply scaling only on X-axis
    return deformed_vertices


def deform_ellipsoid(vertices, left_factor, right_factor):
    """
    Apply different horizontal deformations to the left and right halves.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        left_factor (float): Stretch/compression factor for left side.
        right_factor (float): Stretch/compression factor for right side.

    Returns:
        np.ndarray: Fully deformed vertices.
    """
    vertices_left = deform_half(vertices, left_factor, "left")
    vertices_right = deform_half(
        vertices_left, right_factor, "right"
    )  # Apply right after left
    return vertices_right
