import numpy as np

# Importando as funções necessárias
from modules.geometry.shape_utils import generate_mesh_from_polygon
from modules.geometry.transform_utils import rotate_shape, stretch_one_side
from modules.geometry.ellipsoids import generate_semicircle
from modules.geometry.triangles import generate_triangle


# Função para gerar o triângulo equilátero
# ---------------------------------------------------------------------------- #
# Função para gerar o arquivo STL da combinação do semicírculo e triângulo
def generate_combined_circle_triangle():
    """
    Gera um semicírculo e um triângulo, os combina e gera um arquivo STL.
    """
    # Gerando o semicírculo
    semicircle = generate_semicircle(center=(0, 0), radius=1.0, opening_angle=180)
    # Rotacionando o semicírculo por 90 graus
    semicircle = rotate_shape(semicircle, 90)
    semicircle = stretch_one_side(semicircle, 1.25, "left")

    # Gerando o triângulo
    triangle = generate_triangle(center=(0.0, np.sqrt(3) / 2), side_length=2.0)
    triangle = rotate_shape(triangle, -90)
    triangle = stretch_one_side(triangle, 1.5, "right")

    # Combinando as geometrias (semicírculo + triângulo)
    combined_geometry = semicircle.union(triangle)

    # Gerando o mesh STL a partir da geometria combinada e salvando como 'combined_circle_triangle.stl'
    generate_mesh_from_polygon(
        combined_geometry, stl_filename="combined_circle_triangle.stl"
    )


# Chamada para gerar o STL
generate_combined_circle_triangle()
