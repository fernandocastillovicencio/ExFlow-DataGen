import numpy as np

# Importing necessary functions
from modules.geometry.shape_utils import generate_mesh_from_polygon
from modules.geometry.transform_utils import rotate_shape, stretch_one_side
from modules.geometry.ellipsoids import create_semicircle
from modules.geometry.triangles import generate_triangle


def generate_semicircle():
    semicircle = create_semicircle(center=(0, 0), radius=1.0, opening_angle=180)
    # Rotating the semicircle by 90 degrees and stretching horizontally to the left by 25%
    semicircle = rotate_shape(semicircle, 90)
    return semicircle


def generate_triangle():
    # Generating the triangle
    triangle = generate_triangle(center=(0.0, np.sqrt(3) / 2), side_length=2.0)
    # Rotating the triangle by -90 degrees and stretching horizontally to the right by 50%
    triangle = rotate_shape(triangle, -90)

    return triangle


# Function to generate the equilateral triangle
# ---------------------------------------------------------------------------- #
# Function to generate the STL file of the combined semicircle and triangle
def generate_combined_circle_triangle():
    """
    Generates a semicircle and a triangle, combines them, and generates an STL file.

    The semicircle is generated with center at (0, 0), radius of 1.0, and opening angle of 180 degrees.
    It is then rotated by 90 degrees and stretched horizontally to the left by 25%.

    The triangle is generated with center at (0.0, sqrt(3)/2), side length of 2.0, and is rotated by -90 degrees.
    It is then stretched horizontally to the right by 50%.

    The geometries are combined and rotated by -30 degrees.
    The generated STL file is saved as 'combined_circle_triangle.stl'.
    """
    # ---------------------------------------------------------------------------- #
    semicircle = generate_semicircle()

    semicircle = stretch_one_side(semicircle, "left", 1.25)

    # ---------------------------------------------------------------------------- #
    triangle = generate_triangle()

    # operations
    triangle = stretch_one_side(triangle, "right", 1.5)

    # Combining the geometries (semicircle + triangle)
    combined_geometry = semicircle.union(triangle)
    # Rotating the combined geometry by -30 degrees
    combined_geometry = rotate_shape(combined_geometry, -30)

    # Generating the STL mesh from the combined geometry and saving as 'combined_circle_triangle.stl'
    generate_mesh_from_polygon(
        combined_geometry, stl_filename="combined_circle_triangle.stl"
    )


# Call to generate the STL
generate_combined_circle_triangle()
