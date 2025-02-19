# src/modules/geometry/ellipsoid.py
"""
Generates ellipsoids by applying different deformations and rotations.

This module provides functions to create ellipsoids by generating semicircles,
mirroring them to form full circles, applying horizontal deformations, and rotating
the shapes. The generated ellipsoids are saved as STL and PNG files.

Functions:
- create_ellipsoid(left_factor, right_factor, rotation_angle): Generates an ellipsoid
  by deforming and rotating a circle.
- generate_ellipsoids(): Generates and saves all possible ellipsoids with deformation
  and rotation combinations.

The module ensures that the necessary directories for saving images and STL files exist.
"""

# import numpy as np
# from modules.geometry.semicircles import create_semicircle
from modules.geometry.transform_utils import (
    stretch_both_sides,
    rotate_shape,
)

# from modules.geometry.shape_utils import save_as_stl, save_as_png


# # ---------------------------------------------------------------------------- #
from shapely.geometry import Polygon
import numpy as np


def create_semicircle(center=(0, 0), radius=1.0, opening_angle=180.0, num_points=50):
    """
    Gera um semicírculo com base no centro, raio e ângulo de abertura.

    Parameters:
        center (tuple): Coordenadas (x, y) do centro do círculo (default: (0, 0)).
        radius (float): O raio do círculo (default: 1.0).
        opening_angle (float): O ângulo de abertura do semicírculo (default: 180 graus).
        num_points (int): Número de pontos para gerar o contorno do semicírculo (default: 50).

    Returns:
        Polygon: A geometria do semicírculo como um objeto Shapely Polygon.
    """
    # Definindo os pontos do semicírculo
    theta = np.linspace(
        np.radians(90 - opening_angle / 2),
        np.radians(90 + opening_angle / 2),
        num_points,
    )
    points = [
        (center[0] + radius * np.cos(t), center[1] + radius * np.sin(t)) for t in theta
    ]

    # Criando o polígono (semicírculo)
    semicircle = Polygon(points)

    return semicircle


# # -------------------------------------------------------- #


def create_side_semicircle(side="left"):
    semicircle = create_semicircle()

    if side == "left":
        semicircle = rotate_shape(semicircle, 90)

    elif side == "right":
        semicircle = rotate_shape(semicircle, -90 + 1e-5)

    return semicircle
