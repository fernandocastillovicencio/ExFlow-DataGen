import numpy as np

from shapely.affinity import translate

from modules.geometry.shape_utils import generate_mesh_from_polygon, merge_shapes

from modules.geometry.transform_utils import (
    rotate_shape,
    stretch_one_side,
    translate_shape,
)
from modules.geometry.ellipsoids import create_semicircle, create_side_semicircle
from modules.geometry.triangles import create_triangle, create_side_triangle
from modules.geometry.quadrilaterals import (
    create_square,
    create_side_square,
    create_side_rectangle,
)
from modules.geometry.basic_forms import create_basic_shape


def generate_combined_circle_triangle():

    left_shape = create_basic_shape(shape="rectangle", side="left")
    right_shape = create_basic_shape(shape="rectangle", side="right")

    mix = merge_shapes(left_shape, right_shape)

    mix = create_basic_shape(shape="rectangle", side="left")

    # # ---------------------------------------------------- #
    generate_mesh_from_polygon(mix, stl_filename="combined_circle_triangle.stl")

    print("Generated: combined_circle_triangle.stl")


# Para testes diretos
if __name__ == "__main__":
    generate_combined_circle_triangle()
