# -------------------------------------------------------- #
#                     IMPORT MODULES                       #
# -------------------------------------------------------- #
# Import necessary modules
import numpy as np
from shapely.geometry import Polygon


# -------------------------------------------------------- #
#                        BASIC FORMS                       #
# -------------------------------------------------------- #


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
    theta = np.linspace(np.radians(start_angle), np.radians(end_angle), num=num_points)
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
            (0, height / 2),  # Top vertex
            (-edge / 2, -height / 2),  # Bottom left vertex
            (edge / 2, -height / 2),  # Bottom right vertex
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

    return quadrilateral


# -------------------------------------------------------- #
#                        GENERATION                        #
# -------------------------------------------------------- #
# ---------------------- Ellipsoids ---------------------- #
# Define the generate_ellipsoids function
def generate_ellipsoids():
    """
    Generate an ellipsoid as a Shapely Polygon.

    The ellipsoid is a semicircle with its center at (0, 0) and a radius of 1.0.

    Returns:
        Polygon: A Shapely Polygon object representing the ellipsoid.
    """
    # Create a semicircle (180 degrees) centered at (0, 0)
    ellipsoid = create_circle(start_angle=0, end_angle=180)
    return ellipsoid


# ----------------------- triangles ---------------------- #
# Define the generate_triangles function
def generate_triangles():
    """
    Generate an equilateral triangle as a Shapely Polygon.

    The triangle is centered at (0, 0) with each edge having a length of 2.0.

    Returns:
        Polygon: A Shapely Polygon object representing the triangle.
    """
    triangle = create_triangle(
        edge=2.0
    )  # Create an equilateral triangle with edge length of 2.0
    return triangle


# -------------------- quadrilaterals -------------------- #
# Define the generate_quadrilaterals function
def generate_quadrilaterals():
    """
    Generate a square as a Shapely Polygon.

    The square is centered at (0, 0) with each edge having a length of 2.0.

    Returns:
        Polygon: A Shapely Polygon object representing the square.
    """
    square = create_quadrilateral(edge=2.0)  # Create square
    return square
