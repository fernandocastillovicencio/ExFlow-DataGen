import numpy as np

from shapely.affinity import translate

from modules.geometry.shape_utils import generate_mesh_from_polygon
from modules.geometry.transform_utils import (
    rotate_shape,
    stretch_one_side,
    translate_shape,
)
from modules.geometry.ellipsoids import create_semicircle
from modules.geometry.triangles import create_triangle


def generate_circle_triangle_CT():
    semicircle = create_semicircle()
    semicircle = rotate_shape(semicircle, 90)

    triangle = create_triangle(center=(0.0, np.sqrt(3) / 2), side_length=2.0)
    triangle = rotate_shape(triangle, -90)
    return semicircle, triangle


def generate_circle_triangle_TC():
    semicircle = create_semicircle()
    semicircle = rotate_shape(semicircle, -90)

    triangle = create_triangle()
    triangle = rotate_shape(triangle, 90)
    triangle = translate_shape(triangle, dx=-np.sqrt(3) / 2)

    return semicircle, triangle


def generate_combined_circle_triangle():
    """
    Combina um semicírculo e um triângulo em um único STL.
    """

    semicircle, triangle = generate_circle_triangle_TC()

    semicircle = stretch_one_side(semicircle, "right", 1.5)

    triangle = stretch_one_side(triangle, "left", 1.25)

    combined_geometry = semicircle.union(triangle)
    # combined_geometry = rotate_shape(combined_geometry, -20)

    generate_mesh_from_polygon(
        combined_geometry, stl_filename="combined_circle_triangle.stl"
    )

    print("Generated: combined_circle_triangle.stl")


# Para testes diretos
if __name__ == "__main__":
    generate_combined_circle_triangle()
