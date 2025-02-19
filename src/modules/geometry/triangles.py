"""
Generates triangles by applying different deformations and rotations.

This module provides functions to create triangles, apply horizontal deformations,
and rotate the shapes. The generated triangles are saved as STL files.

Functions:
- create_triangle(): Computes the vertices of an equilateral triangle.
- generate_triangles(): Generates and saves all triangles with deformation and rotation combinations.
"""

import numpy as np
from modules.geometry.transform_utils import (
    rotate_shape,
    stretch_both_sides,
    translate_shape,
)
from modules.geometry.shape_utils import save_as_stl
from shapely.geometry import Polygon


def create_triangle(side_length=2.0):
    """
    Gera um triângulo equilátero com centro em (0, 0) e tamanho da aresta especificado.

    Parameters:
        side_length (float): O tamanho da aresta do triângulo (default: 2.0).

    Returns:
        Polygon: A geometria do triângulo como um objeto Shapely Polygon.
    """
    height = np.sqrt(3) / 2 * side_length
    # As coordenadas dos vértices agora são calculadas com o centro fixo em (0, 0)
    V1 = (0, height / 2)  # Vértice superior
    V2 = (-side_length / 2, -height / 2)  # Vértice inferior esquerdo
    V3 = (side_length / 2, -height / 2)  # Vértice inferior direito

    return Polygon([V1, V2, V3])


# -------------------------------------------------------- #


def create_side_triangle(side="left"):

    triangle = create_triangle()

    if side == "left":
        triangle = rotate_shape(triangle, 90)
        triangle = translate_shape(triangle, dx=-np.sqrt(3) / 2)

    elif side == "right":
        triangle = rotate_shape(triangle, -90)
        triangle = translate_shape(triangle, dx=np.sqrt(3) / 2)

    return triangle


# -------------------------------------------------------- #
