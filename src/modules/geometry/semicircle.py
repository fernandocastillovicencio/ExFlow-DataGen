# src/modules/geometry/semicircle.py
"""
Generates a semicircle geometry.
"""

import numpy as np

def generate_semicircle():
    """
    Compute the vertices and faces of a semicircle.
    
    - Centered at (0,0)
    - Radius = 1
    - Curved edge through (0,1), (-1,0), (0,-1)
    - Straight edge from (0,1) to (0,-1)
    
    Returns:
        tuple: (vertices, faces)
    """
    radius_m = 1.0
    num_points = 50  # Number of points for smooth curvature

    theta = np.linspace(np.pi / 2, 3 * np.pi / 2, num=num_points)
    x = radius_m * np.cos(theta)
    y = radius_m * np.sin(theta)
    z = np.zeros_like(x)

    x_straight = np.array([0, 0])
    y_straight = np.array([1, -1])
    z_straight = np.zeros_like(x_straight)

    vertices = np.column_stack((np.concatenate([x, x_straight]), 
                                np.concatenate([y, y_straight]), 
                                np.concatenate([z, z_straight])))

    faces = [[i, i + 1, len(vertices) - 1] for i in range(len(vertices) - 2)]
    faces.append([len(vertices) - 2, 0, len(vertices) - 1])

    return vertices, faces
