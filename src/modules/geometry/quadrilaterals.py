"""
Generates quadrilaterals by applying different deformations, shears, and rotations.

This module provides functions to create quadrilaterals, apply horizontal deformations,
shears, and rotations. The generated quadrilaterals are saved as STL and PNG files.

Functions:
- create_square(): Creates a square with side length of 1, centered at (0, 0).
- create_rhombus(): Creates a rhombus by rotating the square 45° around (0, 0).
- generate_quadrilaterals(): Generates and saves all quadrilaterals with deformation, shear, and rotation combinations.

The module ensures that the necessary directories for saving images and STL files exist.
"""

import numpy as np
from modules.geometry.transform_utils import (
    stretch_both_sides,
    rotate_shape,
    translate_shape,
)
from modules.geometry.shape_utils import save_as_stl, save_as_png


def create_rhombus():
    """
    Creates a rhombus by rotating the square 45° around (0, 0).

    The rotation is around the origin (0,0) and is counterclockwise.

    Returns:
        tuple: (vertices, faces) - Vertices and faces of the rhombus.
    """
    vertices, faces = create_square()

    # Apply rotation to the square to create a rhombus (losango)
    # The rotation is counterclockwise around the origin (0,0)
    vertices = rotate_shape(vertices, 45)

    return vertices, faces


def generate_quadrilaterals():
    """
    Generate and save quadrilaterals with horizontal shear, stretch, and rotation.

    This function applies horizontal shear, horizontal stretch (both sides), and rotation
    to generate various quadrilaterals and saves them as STL and PNG files.

    The generated quadrilaterals are:

    - Squares and rhombuses with horizontal shear
    - Squares and rhombuses with horizontal stretch (separate factors for left and right sides)
    - Squares and rhombuses with rotation

    The transformations are applied in the order of shear, stretch, and rotation.
    """
    shear_factors = [0.0, 0.1, 0.2, 0.3]  # Shear factors
    deformation_factors = [
        0.75,
        1.0,
        1.5,
        2.0,
    ]  # Deformation factors for both left and right sides
    rotation_angles = [0, 15, 30, 45, 60]  # Rotation angles
    shape_types = [
        "square",
        "rhombus",
    ]  # Two types of initial shapes: square and rhombus

    generated_figures = []  # List to store unique figures

    # Iterate over all combinations of shear, stretch, rotation, and shape type
    for shear_factor in shear_factors:
        for stretch_factor_left in deformation_factors:
            for stretch_factor_right in deformation_factors:
                for rotation_angle in rotation_angles:
                    for shape_type in shape_types:
                        # Create the base shape (square or rhombus)
                        if shape_type == "square":
                            vertices, faces = create_square()
                        elif shape_type == "rhombus":
                            vertices, faces = create_rhombus()

                        # Generate the filename based on the applied transformations
                        filename = f"quadrilateral_Shear{int(shear_factor * 100):03d}_StretchL{int(stretch_factor_left * 100)}_StretchR{int(stretch_factor_right * 100)}_Rot{rotation_angle:03d}"

                        # Apply horizontal shear
                        # The shear is applied before the stretch and rotation
                        vertices = shear_horizontal(vertices, shear_factor)

                        # Apply horizontal stretch (separate factors for left and right)
                        # The stretch is applied after the shear and before the rotation
                        vertices = stretch_both_sides(
                            vertices, stretch_factor_left, stretch_factor_right
                        )

                        # Apply rotation
                        # The rotation is applied after the shear and stretch
                        vertices = rotate_shape(vertices, rotation_angle)

                        # Save the generated shape as both STL and PNG
                        save_as_stl(vertices, faces, filename)
                        save_as_png(vertices, filename)

                        # Add this figure to the list of generated figures
                        generated_figures.append(vertices)


# ---------------------------------------------------------------------------- #
import shapely.geometry as sg
import numpy as np

# -------------------------------------------------------- #
from shapely.geometry import Polygon


def create_square(size=2):
    """
    Cria um quadrado centrado em (0, 0) com o tamanho da aresta especificado.

    O centro é sempre fixo em (0, 0), e a geometria é gerada com o tamanho da aresta dado.
    """
    half_size = size / 2

    # Definir os 4 vértices do quadrado com centro em (0, 0)
    points = [
        (-half_size, -half_size),  # Ponto inferior esquerdo
        (half_size, -half_size),  # Ponto inferior direito
        (half_size, half_size),  # Ponto superior direito
        (-half_size, half_size),  # Ponto superior esquerdo
    ]

    # Criar o polígono quadrado com Shapely
    square = Polygon(points)

    return square

    # ------------------------------------------------------------------------ #


def create_rectangle(width=2, height=1):
    """
    Cria um retângulo centrado em (0, 0) com a largura e altura especificadas.

    Parameters:
        width (float, optional): Largura do retângulo (default: 2).
        height (float, optional): Altura do retângulo (default: 1).

    Returns:
        Polygon: A geometria do retângulo como um objeto Shapely Polygon.
    """
    half_width = width / 2
    half_height = height / 2

    # Definir os 4 vértices do retângulo com centro em (0, 0)
    points = [
        (-half_width, -half_height),  # Inferior esquerdo
        (half_width, -half_height),  # Inferior direito
        (half_width, half_height),  # Superior direito
        (-half_width, half_height),  # Superior esquerdo
    ]

    # Criar o polígono retangular com Shapely
    rectangle = Polygon(points)

    return rectangle


# -------------------------------------------------------- #
def create_side_square(side="left"):

    square = create_square()

    if side == "left":
        square = translate_shape(square, dx=-1.0 + 1e-5)

    elif side == "right":
        square = translate_shape(square, dx=1.0 - 1e-5)

    return square


# -------------------------------------------------------- #
def create_side_rectangle(side="left"):

    rectangle = create_rectangle(width=1, height=2)

    if side == "left":
        rectangle = translate_shape(rectangle, dx=-0.5 + 1e-5)

    elif side == "right":
        rectangle = translate_shape(rectangle, dx=0.5 - 1e-5)

    return rectangle
