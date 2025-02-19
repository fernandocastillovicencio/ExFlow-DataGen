# Import necessary modules
import numpy as np

# Import merge_shapes function from modules.geometry.shape_utils
from modules.geometry.shape_utils import merge_shapes

# Import shape creation functions from modules.geometry.simples_shapes
from modules.geometry.simples_shapes import (
    create_circle,  # Import create_circle function
    create_triangle,  # Import create_triangle function
    create_quadrilateral,  # Import create_quadrilateral function
)

# Define tolerance value
tol = 1e-6


# -------------------------------------------------------- #
#                      STARTING SHAPES                     #
# -------------------------------------------------------- #
# Define the create_starting_shape function
def create_starting_shape(shape="semicircle", side="left"):
    """
    Create a shape (circle or triangle) based on the provided arguments.

    Parameters
    ----------
    shape : str, optional
        The shape to create, either 'circle' or 'triangle'. Defaults to 'circle'.
    side : str, optional
        The side of the shape to create. Defaults to 'left'.

    Returns
    -------
    Polygon
        The generated shape as a Shapely Polygon object.
    """

    # Check if shape is circle
    if shape == "circle":
        if side == "left":
            shape = create_circle(
                start_angle=90, end_angle=270
            )  # Create left semicircle
        elif side == "right":
            shape = create_circle(
                start_angle=-90, end_angle=90
            )  # Create right semicircle

    # Check if shape is triangle
    elif shape == "triangle":
        height = np.sqrt(3)  # Calculate height of the triangle
        if side == "left":
            shape = create_triangle(
                vertices=[(0.0 + tol, -1), (0.0 + tol, 1), (-height, 0)]
            )  # Create left triangle
        elif side == "right":
            shape = create_triangle(
                vertices=[(0.0 - tol, -1), (0.0 - tol, 1), (height, 0)]
            )  # Create right triangle

    # Check if shape is square
    elif shape == "square":
        ymin = -1.0
        ymax = 1.0
        if side == "left":
            xmin = -1.0
            xmax = 0.0 + tol
        elif side == "right":
            xmin = 0.0 - tol
            xmax = 1.0
        shape = create_quadrilateral(
            vertices=[
                (xmin, ymin),
                (xmax, ymin),
                (xmax, ymax),
                (xmin, ymax),
            ]
        )  # Create square

    else:
        shape = None
        raise ValueError("The argument 'shape' must be 'semicircle' or 'shape'.")

    return shape


# -------------------------------------------------------- #
#                        GENERATING                        #
# -------------------------------------------------------- #
# Define the generate_combined_circle_triangle function
def generate_combined_circle_triangle():
    """
    Generate a combined shape consisting of a circle and a triangle.

    The circle is on the left side, and the triangle is on the right side.

    Returns:
        Polygon: The combined shape.
    """
    left_shape = create_starting_shape(
        shape="circle", side="left"
    )  # Create left semicircle
    right_shape = create_starting_shape(
        shape="triangle", side="right"
    )  # Create right triangle
    combined = merge_shapes(left_shape, right_shape)  # Merge shapes
    return combined


# Define the generate_combined_circle_square function
def generate_combined_circle_square():
    """
    Generate a combined shape consisting of a circle and a square.

    The square is on the left side, and the circle is on the right side.

    Returns:
        Polygon: The combined shape.
    """
    left_shape = create_starting_shape(
        shape="square", side="left"
    )  # Create left square
    right_shape = create_starting_shape(
        shape="circle", side="right"
    )  # Create right semicircle
    combined = merge_shapes(left_shape, right_shape)  # Merge shapes
    return combined


# Define the generate_combined_triangle_square function
def generate_combined_triangle_square():
    """
    Generate a combined shape consisting of a triangle and a square.

    The triangle is on the left side, and the square is on the right side.

    Returns:
        Polygon: The combined shape.
    """
    left_shape = create_starting_shape(
        shape="triangle", side="left"
    )  # Create left triangle
    right_shape = create_starting_shape(
        shape="square", side="right"
    )  # Create right square
    combined = merge_shapes(left_shape, right_shape)  # Merge shapes
    return combined
