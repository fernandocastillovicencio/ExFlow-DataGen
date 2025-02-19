# Import necessary functions from modules.geometry.simples_shapes
from modules.geometry.simples_shapes import (
    generate_ellipsoids,
    generate_triangles,
    generate_quadrilaterals,
)

# Import necessary functions from modules.geometry.combined_shapes
from modules.geometry.combined_shapes import (
    generate_combined_circle_triangle,
    generate_combined_circle_square,
    generate_combined_triangle_square,
)

from modules.geometry.shape_utils import generate_mesh_from_polygon


# -------------------------------------------------------- #
#                    GENERATE OBSTACLES                    #
# -------------------------------------------------------- #
# Define the generate_obstacles function
def generate_obstacles():
    """
    Test the obstacle generation loop by printing categories and shapes without executing the functions.

    This function is used to generate obstacles by looping through categories
    and subcategories, and generating the shapes using the corresponding
    functions. The generated shapes are then saved as .stl files with the
    shape name as the filename.

    The categories and their respective functions are defined in the
    categories dictionary. The keys of the dictionary are the categories,
    and the values are lists of tuples, where the first element of the tuple
    is the shape name, and the second element is the function used to generate
    the shape.
    """
    # Define categories dictionary with simple and combined shapes
    categories = {
        "simple": [
            ("ellipsoid", generate_ellipsoids),  # Simple shape: ellipsoid
            ("triangle", generate_triangles),  # Simple shape: triangle
            ("quadrilateral", generate_quadrilaterals),  # Simple shape: quadrilateral
        ],
        "combined": [
            (
                "circle-triangle",
                generate_combined_circle_triangle,
            ),  # Combined shape: circle-triangle
            (
                "circle-square",
                generate_combined_circle_square,
            ),  # Combined shape: circle-square
            (
                "triangle-square",
                generate_combined_triangle_square,
            ),  # Combined shape: triangle-square
        ],
    }

    # Loop through categories and subcategories
    for category, subcategories in categories.items():
        print(f"Generating obstacles in category: {category}")  # Print category
        for shape_name, generation in subcategories:
            print(f"Generating {shape_name} shape")  # Print shape name
            shape = generation()  # Generate shape
            print(f"Saving {shape_name} shape as {shape_name}.stl file")
            generate_mesh_from_polygon(
                shape, stl_filename=shape_name + ".stl"
            )  # Generate mesh from polygon and save as .stl file


# Direct script execution
if __name__ == "__main__":
    generate_obstacles()  # Call generate_obstacles function
