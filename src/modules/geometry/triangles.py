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
)
from modules.geometry.shape_utils import save_as_stl
from shapely.geometry import Polygon


def create_triangle(center=(0, 0), side_length=2.0):
    """
    Gera um triângulo equilátero com base no centro e no tamanho da aresta.

    Parameters:
        center (tuple): Coordenadas (x, y) do centro do triângulo (default: (0, 0)).
        side_length (float): O tamanho da aresta do triângulo (default: 2.0).

    Returns:
        Polygon: A geometria do triângulo como um objeto Shapely Polygon.
    """
    height = np.sqrt(3) / 2 * side_length
    V1 = (center[0], center[1] + height / 2)
    V2 = (center[0] - side_length / 2, center[1] - height / 2)
    V3 = (center[0] + side_length / 2, center[1] - height / 2)

    return Polygon([V1, V2, V3])


def generate_triangles():
    """
    Generate and save all triangles with various stretch and rotation transformations.
    """
    stretch_factors = [0.75, 1.0, 1.5, 2.0]
    rotation_angles = [0, 15, 30, 45, 60, 75]

    for left_factor in stretch_factors:
        for right_factor in stretch_factors:
            for angle in rotation_angles:
                triangle = create_triangle()
                triangle = stretch_both_sides(triangle, left_factor, right_factor)
                triangle = rotate_shape(triangle, angle)

                filename = f"triangle_L{int(left_factor * 100)}_R{int(right_factor * 100)}_Rot{angle}.stl"
                save_as_stl(triangle, filename)

                print(f"Generated: {filename}")


# Para testes diretos
if __name__ == "__main__":
    generate_triangles()
