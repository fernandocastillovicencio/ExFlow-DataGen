# -------------------------------------------------------- #
#                     IMPORT MODULES                       #
# -------------------------------------------------------- #
# Import necessary modules
import numpy as np
import os
from shapely.geometry import Polygon

from modules.geometry.transform_utils import (
    stretch_one_side,
    stretch_both_sides,
    rotate_shape,
)
from modules.geometry.shape_utils import save_files

# -------------------------------------------------------- #
#                         PREAMBLE                         #
# -------------------------------------------------------- #
# Define directories
IMAGE_DIR = "geometries/obstacles/images"
STL_DIR = "geometries/obstacles/stl"

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(STL_DIR, exist_ok=True)


# -------------------------------------------------------- #
#                        BASIC FORMS                       #
# -------------------------------------------------------- #
tol = 1e-6


# ------------------------ circle ------------------------ #
# Define the create_circle function
def create_circle(
    center=(0, 0),
    radius=1.0,
    start_angle=0,
    end_angle=None,
    num_points=100,
):
    """
    Create a circular shape using Shapely's Polygon class.

    Parameters:
        center (tuple): Coordinates of the circle's center (x, y).
        radius (float): The circle's radius.
        start_angle (float): The angle at which the circle starts (in degrees).
        end_angle (float): The angle at which the circle ends (in degrees).
            If not provided, the function will create a full circle (360 degrees).
        num_points (int): The number of points to generate along the circumference.

    Returns:
        Polygon: The generated circle as a Polygon object.

    Raises:
        ValueError: If the end angle is not greater than the start angle.
    """
    # If end_angle is not provided, set it to 360 to create a full circle
    if end_angle is None:
        end_angle = 360  # Full circle
    elif start_angle >= end_angle:
        raise ValueError("The end angle must be greater than the start angle.")

    # Generate points along the circumference based on start and end angles
    theta = np.linspace(
        np.radians(start_angle - tol), np.radians(end_angle + tol), num=num_points
    )
    x = radius * np.cos(theta) + center[0]
    y = radius * np.sin(theta) + center[1]

    # Create the polygon (circular, semicircular, or arc)
    points = list(zip(x, y))

    # To ensure the shape is closed, add the first point to the end
    points.append(points[0])  # Add the first point at the end to close the shape

    # Create the Polygon with Shapely
    circle = Polygon(points)

    return circle


# ----------------------- triangle ----------------------- #
# Define the create_triangle function
def create_triangle(**kwargs):
    """
    Create a triangle as a Shapely Polygon.

    Parameters:
        vertices (list of tuple): A list of 3 vertices (x, y) to define the triangle.
        edge (float): The length of the edge for an equilateral triangle centered at (0, 0).

    Returns:
        Polygon: A Shapely Polygon object representing the triangle.

    Raises:
        ValueError: If neither 'vertices' nor 'edge' is provided, or if their conditions are not met.
    """
    if "vertices" in kwargs:
        # Use provided vertices if available
        vertices = kwargs["vertices"]
        if len(vertices) != 3:
            raise ValueError(
                "If 'vertices' is provided, it must be a list with 3 vertices."
            )
    elif "edge" in kwargs:
        # Create an equilateral triangle if 'edge' is provided
        edge = kwargs["edge"]
        if edge <= 0:
            raise ValueError("The value of 'edge' must be greater than 0.")
        # Calculate the height of the equilateral triangle
        height = np.sqrt(3) / 2 * edge
        # Define vertices for an equilateral triangle centered at (0, 0)
        vertices = [
            (0, -height / 2),  # Bottom vertex (antes era topo)
            (-edge / 2, height / 2),  # Top left vertex (antes era bottom left)
            (edge / 2, height / 2),  # Top right vertex (antes era bottom right)
        ]

    else:
        raise ValueError("The function needs a 'vertices' or 'edge' parameter.")

    # Create the Polygon with Shapely using the defined vertices
    triangle = Polygon(vertices)

    return triangle


# --------------------- quadrilateral -------------------- #
# Define the create_quadrilateral function
def create_quadrilateral(**kwargs):
    """
    Create a quadrilateral as a Shapely Polygon.

    Parameters:
        vertices (list of tuple): A list of 4 vertices (x, y) to define the quadrilateral.
        edge (float): The length of the edge for a square centered at (0, 0).

    Returns:
        Polygon: A Shapely Polygon object representing the quadrilateral.

    Raises:
        ValueError: If neither 'vertices' nor 'edge' is provided, or if their conditions are not met.
    """
    if "vertices" in kwargs:
        # Use the provided vertices if available
        vertices = kwargs["vertices"]
        if len(vertices) != 4:
            raise ValueError(
                "If 'vertices' is provided, it must be a list with 4 vertices."
            )
    elif "edge" in kwargs:
        # Create a square if 'edge' is provided
        edge = kwargs["edge"] if kwargs["edge"] is not None else 1  # Default: 1
        if edge <= 0:
            raise ValueError("The value of 'edge' must be greater than 0.")
        # Define vertices for a square centered at (0, 0)
        vertices = [
            (edge / 2, edge / 2),  # Top right vertex
            (-edge / 2, edge / 2),  # Top left vertex
            (-edge / 2, -edge / 2),  # Bottom left vertex
            (edge / 2, -edge / 2),  # Bottom right vertex
        ]
    else:
        raise ValueError("The function needs a 'vertices' or 'edge' parameter.")

    # Create the Polygon with Shapely using the defined vertices
    quadrilateral = Polygon(vertices)

    return quadrilateral


# -------------------------------------------------------- #
#                        GENERATION                        #
# -------------------------------------------------------- #
# ---------------------- Ellipsoids ---------------------- #
# Define the generate_ellipsoids function
def generate_ellipsoids():
    """
    Generate an ellipsoid as a Shapely Polygon with variations.

    Avoids redundant cases where both stretch factors are 1.0, meaning the shape remains a circle.

    Returns:
        Polygon: The last generated Shapely Polygon.
    """
    # Definições dos valores de alongamento/compressão e ângulos de rotação
    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Fatores de alongamento/compressão
    rotation_angles = [0, 15, 30, 45, 60, 75]  # Ângulos de rotação

    # Criar um círculo inicial
    circle = create_circle()

    # Gerar todas as combinações de alongamento e rotação
    for right_stretch in stretch_factors:
        for left_stretch in stretch_factors:
            # Aplicar alongamento nos dois lados
            right_long = stretch_one_side(circle, "right", right_stretch)
            left_long = stretch_one_side(right_long, "left", left_stretch)

            # Caso normal: Aplicar rotações
            for angle in rotation_angles:
                rotated = rotate_shape(left_long, angle)
                if left_stretch == 1.0 and right_stretch == 1.0 and angle != 0.0:
                    pass
                else:
                    save_files(rotated, "ellipsoid", left_stretch, right_stretch, angle)

    return rotated


# ---------------------- Semicircles --------------------- #
# Define the generate_ellipsoids function
def generate_semicircles():
    """
    Generate a semicircle as a Shapely Polygon.

    The semicircle is centered at (0, 0) with a radius of 1.0, and spans 180 degrees.

    Returns:
        Polygon: A Shapely Polygon object representing the semicircle.
    """

    # ---------------------------------------------------- #
    # semicircle = create_circle(start_angle=90, end_angle=270)
    # ---------------------------------------------------- #

    # Definições dos valores de alongamento/compressão e ângulos de rotação
    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Fatores de alongamento/compressão
    rotation_angles = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]
    # Ângulos de rotação

    # Criar um círculo inicial
    semicircle = create_circle(start_angle=90, end_angle=270)

    # Gerar todas as combinações de alongamento e rotação
    for stretch in stretch_factors:

        left_long = stretch_both_sides(semicircle, stretch)
        # Caso normal: Aplicar rotações
        for angle in rotation_angles:
            rotated = rotate_shape(left_long, angle)
            save_files(rotated, "semicircle", stretch, 0.0, angle)

    return rotated


# ----------------------- triangles ---------------------- #
# Define the generate_triangles function
def generate_triangles():
    """
    Generate an equilateral triangle as a Shapely Polygon.

    The triangle is centered at (0, 0) with each edge having a length of 2.0.

    Returns:
        Polygon: A Shapely Polygon object representing the triangle.
    """
    # ---------------------------------------------------- #
    # triangle = create_triangle(edge=2.0)
    # Create an equilateral triangle with edge length of 2.0
    # ---------------------------------------------------- #

    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Fatores de alongamento/compressão
    rotation_angles = [0, 10, 20, 30, 40, 50, 60, 75, 90, 105, 120]

    # Criar um círculo inicial
    triangle = create_triangle(edge=2.0)

    # Gerar todas as combinações de alongamento e rotação
    for right_stretch in stretch_factors:
        for left_stretch in stretch_factors:
            # Aplicar alongamento nos dois lados
            right_long = stretch_one_side(triangle, "right", right_stretch)
            left_long = stretch_one_side(right_long, "left", left_stretch)

            # Caso normal: Aplicar rotações
            for angle in rotation_angles:
                rotated = rotate_shape(left_long, angle)

                save_files(rotated, "triangle", left_stretch, right_stretch, angle)

    return rotated


# -------------------- quadrilaterals -------------------- #
# Define the generate_quadrilaterals function
def generate_quadrilaterals(rhombus=False):
    """
    Generate a square as a Shapely Polygon.

    The square is centered at (0, 0) with each edge having a length of 2.0.

    Returns:
        Polygon: A Shapely Polygon object representing the square.
    """

    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Fatores de alongamento/compressão
    rotation_angles = [0, 15, 30, 45, 60, 75]

    # ---------------------- square ---------------------- #
    square = create_quadrilateral(edge=2.0)

    for stretch in stretch_factors:
        long = stretch_both_sides(square, stretch)

        for angle in rotation_angles:
            rotated = rotate_shape(long, angle)

            save_files(rotated, "rectangle", stretch, stretch, angle)

    # ---------------------- rhombus --------------------- #

    rhombus = create_quadrilateral(vertices=[(0, 1), (-1, 0), (0, -1), (1, 0)])

    for left_stretch in stretch_factors:
        left_long = stretch_one_side(rhombus, "left", left_stretch)

        for right_stretch in stretch_factors:
            right_long = stretch_one_side(left_long, "right", right_stretch)

            for angle in rotation_angles:
                rotated = rotate_shape(right_long, angle)

                if left_stretch == 1.0 and right_stretch == 1.0:
                    pass
                else:
                    save_files(rotated, "rhombus", left_stretch, right_stretch, angle)
                    # pass

    # ---------------------------------------------------- #
    return rotated
