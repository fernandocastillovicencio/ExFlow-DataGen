# Import necessary modules
import numpy as np  # Import NumPy for numerical operations
from shapely.geometry import (
    Polygon,
)  # Import Polygon from Shapely for geometric operations

# Import functions from transform_utils
from modules.geometry.transform_utils import (
    stretch_one_side,  # Import stretch_one_side function
    stretch_both_sides,  # Import stretch_both_sides function
    rotate_shape,  # Import rotate_shape function
)

# Import save_files function from shape_utils
from modules.geometry.shape_utils import save_files  # Import save_files function

# Define tolerance value
tol = 1e-6  # Set tolerance value for angle calculations


# Define the create_circle function
def create_circle(
    center=(0, 0),  # Default center of the circle
    radius=1.0,  # Default radius of the circle
    start_angle=0,  # Default start angle of the circle
    end_angle=None,  # Default end angle of the circle
    num_points=100,  # Default number of points along the circumference
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
    tol = 1e-6
    # If end_angle is not provided, set it to 360 to create a full circle
    if end_angle is None:  # Check if end_angle is None
        end_angle = 360  # Full circle
        tol = 0.0
    elif (
        start_angle >= end_angle
    ):  # Check if start_angle is greater than or equal to end_angle
        raise ValueError(
            "The end angle must be greater than the start angle."
        )  # Raise an error if end_angle is invalid

    # Generate points along the circumference based on start and end angles
    theta = np.linspace(
        np.radians(start_angle - tol),
        np.radians(end_angle + tol),
        num=num_points,  # Generate angles in radians
    )
    x = radius * np.cos(theta) + center[0]  # Calculate x-coordinates of points
    y = radius * np.sin(theta) + center[1]  # Calculate y-coordinates of points

    # Create the polygon (circular, semicircular, or arc)
    points = list(zip(x, y))  # Combine x and y coordinates into points

    # To ensure the shape is closed, add the first point to the end
    points.append(points[0])  # Add the first point at the end to close the shape

    # Create the Polygon with Shapely
    circle = Polygon(points)  # Create the Polygon object

    return circle  # Return the created circle


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
    if "vertices" in kwargs:  # Check if vertices are provided
        # Use provided vertices if available
        vertices = kwargs["vertices"]  # Get vertices from kwargs
        if len(vertices) != 3:  # Check if the number of vertices is 3
            raise ValueError(
                "If 'vertices' is provided, it must be a list with 3 vertices."  # Raise an error if vertices are invalid
            )
    elif "edge" in kwargs:  # Check if edge is provided
        # Create an equilateral triangle if 'edge' is provided
        edge = kwargs["edge"]  # Get edge length from kwargs
        if edge <= 0:  # Check if edge length is valid
            raise ValueError(
                "The value of 'edge' must be greater than 0."
            )  # Raise an error if edge length is invalid
        # Calculate the height of the equilateral triangle
        height = np.sqrt(3) / 2 * edge  # Calculate height of the triangle
        # Define vertices for an equilateral triangle centered at (0, 0)
        vertices = [
            (0, -height / 2),  # Bottom vertex
            (-edge / 2, height / 2),  # Top left vertex
            (edge / 2, height / 2),  # Top right vertex
        ]

    else:  # If neither vertices nor edge is provided
        raise ValueError(
            "The function needs a 'vertices' or 'edge' parameter."
        )  # Raise an error if parameters are missing

    # Create the Polygon with Shapely using the defined vertices
    triangle = Polygon(vertices)  # Create the Polygon object

    return triangle  # Return the created triangle


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
    if "vertices" in kwargs:  # Check if vertices are provided
        # Use the provided vertices if available
        vertices = kwargs["vertices"]  # Get vertices from kwargs
        if len(vertices) != 4:  # Check if the number of vertices is 4
            raise ValueError(
                "If 'vertices' is provided, it must be a list with 4 vertices."  # Raise an error if vertices are invalid
            )
    elif "edge" in kwargs:  # Check if edge is provided
        # Create a square if 'edge' is provided
        edge = (
            kwargs["edge"] if kwargs["edge"] is not None else 1
        )  # Default: 1  # Get edge length from kwargs or set default
        if edge <= 0:  # Check if edge length is valid
            raise ValueError(
                "The value of 'edge' must be greater than 0."
            )  # Raise an error if edge length is invalid
        # Define vertices for a square centered at (0, 0)
        vertices = [
            (edge / 2, edge / 2),  # Top right vertex
            (-edge / 2, edge / 2),  # Top left vertex
            (-edge / 2, -edge / 2),  # Bottom left vertex
            (edge / 2, -edge / 2),  # Bottom right vertex
        ]
    else:  # If neither vertices nor edge is provided
        raise ValueError(
            "The function needs a 'vertices' or 'edge' parameter."
        )  # Raise an error if parameters are missing

    # Create the Polygon with Shapely using the defined vertices
    quadrilateral = Polygon(vertices)  # Create the Polygon object

    return quadrilateral  # Return the created quadrilateral


# Define the generate_ellipsoids function
def generate_ellipsoids():
    """
    Generate an ellipsoid as a Shapely Polygon with variations.

    Avoids redundant cases where both stretch factors are 1.0, meaning the shape remains a circle.

    Returns:
        Polygon: The last generated Shapely Polygon.
    """
    # Definitions of stretch/compression values and rotation angles
    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [0, 15, 30, 45, 60, 75]  # Rotation angles

    # Create an initial circle
    circle = create_circle()  # Create a circle

    # Generate all combinations of stretch and rotation
    for right_stretch in stretch_factors:  # Loop through right stretch factors
        for left_stretch in stretch_factors:  # Loop through left stretch factors
            # Apply stretch on both sides
            right_long = stretch_one_side(
                circle, "right", right_stretch
            )  # Stretch the right side
            left_long = stretch_one_side(
                right_long, "left", left_stretch
            )  # Stretch the left side

            # Normal case: Apply rotations
            for angle in rotation_angles:  # Loop through rotation angles
                rotated = rotate_shape(left_long, angle)  # Rotate the shape
                if (
                    left_stretch == 1.0 and right_stretch == 1.0 and angle != 0.0
                ):  # Check if the shape is unchanged
                    pass  # Skip saving the unchanged shape
                else:  # If the shape is changed
                    save_files(
                        rotated, "ellipsoid", left_stretch, right_stretch, angle
                    )  # Save the shape

    return rotated  # Return the last generated shape


# Define the generate_semicircles function
def generate_semicircles():
    """
    Generate a semicircle as a Shapely Polygon.

    The semicircle is centered at (0, 0) with a radius of 1.0, and spans 180 degrees.

    Returns:
        Polygon: A Shapely Polygon object representing the semicircle.
    """
    # Definitions of stretch/compression values and rotation angles
    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [
        0,
        15,
        30,
        45,
        60,
        75,
        90,
        105,
        120,
        135,
        150,
        165,
        180,
        75,
        90,
        105,
        120,
        135,
        150,
        165,
        180,
    ]  # Rotation angles

    # Create an initial semicircle
    semicircle = create_circle(start_angle=90, end_angle=270)

    # Generate all combinations of stretch and rotation
    for stretch in stretch_factors:
        left_long = stretch_both_sides(semicircle, stretch)
        # Normal case: Apply rotations
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
    # Definitions of stretch/compression values and rotation angles
    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [0, 10, 20, 30, 40, 50, 60, 75, 90, 105, 120]  # Rotation angles

    # Create an initial equilateral triangle with edge length of 2.0
    triangle = create_triangle(edge=2.0)

    # Generate all combinations of stretch and rotation
    for right_stretch in stretch_factors:
        for left_stretch in stretch_factors:
            # Apply stretch on both sides
            right_long = stretch_one_side(triangle, "right", right_stretch)
            left_long = stretch_one_side(right_long, "left", left_stretch)

            # Normal case: Apply rotations
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
    # Definitions of stretch/compression values and rotation angles
    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [0, 15, 30, 45, 60, 75]  # Rotation angles

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

    return rotated
