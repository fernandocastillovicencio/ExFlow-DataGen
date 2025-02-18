import numpy as np
from modules.geometry.shape_utils import generate_mesh_from_polygon
from modules.geometry.transform_utils import rotate_shape, stretch_one_side
from modules.geometry.ellipsoids import create_semicircle
from modules.geometry.triangles import create_triangle


def generate_semicircle():
    semicircle = create_semicircle(center=(0, 0), radius=1.0, opening_angle=180)
    semicircle = rotate_shape(semicircle, 90)
    return semicircle


def generate_triangle():
    triangle = create_triangle(center=(0.0, np.sqrt(3) / 2), side_length=2.0)
    triangle = rotate_shape(triangle, -90)
    return triangle


def generate_combined_circle_triangle():
    """
    Combina um semicírculo e um triângulo em um único STL.
    """
    semicircle = generate_semicircle()  # Chamar a função corretamente
    semicircle = stretch_one_side(semicircle, "left", 1.25)

    triangle = generate_triangle()
    triangle = stretch_one_side(triangle, "right", 1.5)

    combined_geometry = semicircle.union(triangle)
    combined_geometry = rotate_shape(combined_geometry, -30)

    generate_mesh_from_polygon(
        combined_geometry, stl_filename="combined_circle_triangle.stl"
    )

    print("Generated: combined_circle_triangle.stl")


# Para testes diretos
if __name__ == "__main__":
    generate_combined_circle_triangle()
