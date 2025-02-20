# Import necessary modules
import numpy as np

# Import merge_shapes function from modules.geometry.shape_utils
from modules.geometry.shape_utils import merge_shapes, save_files
from modules.geometry.transform_utils import stretch_one_side, rotate_shape

# Import shape creation functions from modules.geometry.simples_shapes
from modules.geometry.simples_shapes import (
    create_circle,  # Import create_circle function
    create_triangle,  # Import create_triangle function
    create_quadrilateral,  # Import create_quadrilateral function
)

# Define tolerance value
tol = 1e-6


# ---------------------- STARTING SHAPES ---------------------- #
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
        )
        # Create square

    else:
        shape = None
        raise ValueError("The argument 'shape' must be 'semicircle' or 'shape'.")

    return shape


# ---------------------- GENERATING ---------------------- #
# Define the generate_combined_circle_triangle function
def generate_combined_circle_triangle():
    """
    Generate a combined shape consisting of a circle and a triangle.

    The circle is on the left side, and the triangle is on the right side.

    The function generates a combination of both shapes with different stretch factors
    and rotation angles, and saves the resulting shapes as STL and PNG files.

    The function returns the last generated shape as a Shapely Polygon object.

    Returns:
        Polygon: The combined shape.
    """
    shape1 = "circle"
    shape2 = "triangle"

    order = [(shape1, shape2, "1"), (shape2, shape1, "2")]

    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [0, 15, 30, 45, 60, 75]

    for i in range(2):
        left_type, right_type, index = order[i]

        left_shape = create_starting_shape(shape=left_type, side="left")
        right_shape = create_starting_shape(shape=right_type, side="right")

        for right_stretch in stretch_factors:
            right_long = stretch_one_side(right_shape, "right", right_stretch)
            for left_stretch in stretch_factors:
                # Apply stretch on both sides
                left_long = stretch_one_side(left_shape, "left", left_stretch)

                combined = merge_shapes(left_long, right_long)
                # Normal case: Apply rotations
                for angle in rotation_angles:
                    rotated = rotate_shape(combined, angle)
                    save_files(
                        rotated,
                        "combined_" + shape1 + "_" + shape2 + index,
                        left_stretch,
                        right_stretch,
                        angle,
                    )
    return combined


# Define the generate_combined_circle_square function
def generate_combined_circle_square():
    """
    Generate a combined shape consisting of a circle and a square.

    The square is on the left side, and the circle is on the right side.

    Returns:
        Polygon: The combined shape.
    """
    shape1 = "circle"
    shape2 = "square"

    order = [(shape1, shape2, "1"), (shape2, shape1, "2")]

    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [0, 15, 30, 45, 60, 75]

    for i in range(2):
        left_type, right_type, index = order[i]

        left_shape = create_starting_shape(shape=left_type, side="left")
        right_shape = create_starting_shape(shape=right_type, side="right")

        for right_stretch in stretch_factors:
            right_long = stretch_one_side(right_shape, "right", right_stretch)
            for left_stretch in stretch_factors:
                # Apply stretch on both sides
                left_long = stretch_one_side(left_shape, "left", left_stretch)

                combined = merge_shapes(left_long, right_long)
                # Normal case: Apply rotations
                for angle in rotation_angles:
                    rotated = rotate_shape(combined, angle)
                    save_files(
                        rotated,
                        "combined_" + shape1 + "_" + shape2 + index,
                        left_stretch,
                        right_stretch,
                        angle,
                    )
    return combined


# Define the generate_combined_triangle_square function
def generate_combined_triangle_square():
    """
    Generate a combined shape consisting of a triangle and a square.

    The triangle is on the left side, and the square is on the right side.

    Returns:
        Polygon: The combined shape.
    """
    shape1 = "triangle"
    shape2 = "square"

    order = [(shape1, shape2, "1"), (shape2, shape1, "2")]

    stretch_factors = [0.75, 1.0, 1.5, 2.0]  # Stretch/compression factors
    rotation_angles = [0, 15, 30, 45, 60, 75]

    for i in range(2):
        left_type, right_type, index = order[i]

        left_shape = create_starting_shape(shape=left_type, side="left")
        right_shape = create_starting_shape(shape=right_type, side="right")

        for right_stretch in stretch_factors:
            right_long = stretch_one_side(right_shape, "right", right_stretch)
            for left_stretch in stretch_factors:
                # Apply stretch on both sides
                left_long = stretch_one_side(left_shape, "left", left_stretch)

                combined = merge_shapes(left_long, right_long)
                # Normal case: Apply rotations
                for angle in rotation_angles:
                    rotated = rotate_shape(combined, angle)
                    save_files(
                        rotated,
                        "combined_" + shape1 + "_" + shape2 + index,
                        left_stretch,
                        right_stretch,
                        angle,
                    )
    return combined
