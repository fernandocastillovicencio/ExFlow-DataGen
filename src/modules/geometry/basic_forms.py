import numpy as np
from shapely.geometry import Polygon
from modules.geometry.transform_utils import rotate_shape, translate_shape

from modules.geometry.ellipsoids import create_semicircle
from modules.geometry.triangles import create_triangle
from modules.geometry.quadrilaterals import create_rectangle

# -------------------------------------------------------- #


# -------------------------------------------------------- #


# -------------------------------------------------------- #


# -------------------------------------------------------- #
#                       DERIVED FORMS                      #
# -------------------------------------------------------- #


def create_basic_shape(shape="semicircle", side="left"):
    """
    Creates a basic shape (semicircle or shape) with the specified side.

    Parameters:
        shape (str): The basic shape to create: 'semicircle' or 'shape'.
        side (str): The side of the shape to create: 'left' or 'right'.

    Returns:
        Polygon: The basic shape with the specified side.
    """

    if shape == "semicircle":
        shape = create_semicircle()

        if side == "left":
            shape = rotate_shape(shape, 90 - 1e-5)

        elif side == "right":
            shape = rotate_shape(shape, -90 + 1e-5)

    elif shape == "triangle":
        shape = create_triangle()

        if side == "left":
            shape = rotate_shape(shape, 90)
            shape = translate_shape(shape, dx=-np.sqrt(3) / 2)

        elif side == "right":
            shape = rotate_shape(shape, -90)
            shape = translate_shape(shape, dx=np.sqrt(3) / 2)

    elif shape == "rectangle":
        shape = create_rectangle(width=1, height=2)

        if side == "left":
            shape = translate_shape(shape, dx=-0.5 + 1e-5)

        elif side == "right":
            shape = translate_shape(shape, dx=0.5 - 1e-5)

        return shape

    else:
        shape = None
        raise ValueError("The argument 'shape' must be 'semicircle' or 'shape'.")

    return shape
