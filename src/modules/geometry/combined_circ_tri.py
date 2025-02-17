import os

from modules.geometry.ellipsoids import create_semicircle
from modules.geometry.quadrilaterals import create_square
from modules.geometry.shape_utils import create_mesh_from_shape

# Define directories
IMAGE_DIR = "geometries/obstacles/images"
STL_DIR = "geometries/obstacles/stl"


def generate_semicircle():
    # Gerar o semicírculo
    semicircle = create_semicircle(radius=1, num_points=50)

    # Criar a malha para o semicírculo
    mesh = create_mesh_from_shape(semicircle)

    # Salvar a malha como um arquivo STL
    filename = f"semicircle"

    stl_path = os.path.join(STL_DIR, f"{filename}.stl")
    mesh.export(stl_path)

    print(f"Arquivo STL salvo como '{filename}'.")


# ---------------------------------------------------------------------------- #


def generate_square():
    print("Generating square of size 1 centered at (0, 0)")

    # Gerar o quadrado com tamanho 1 centrado em (0, 0)
    square = create_square(size=1, center=(0, 0))

    # Criar a malha para o quadrado
    mesh = create_mesh_from_shape(square)

    # Salvar a malha como um arquivo STL
    filename = "geometries/obstacles/stl/square.stl"
    mesh.export(filename)
    print(f"Arquivo STL salvo como '{filename}'.")


# ---------------------------------------------------------------------------- #
def generate_combined_circle_triangle():
    print("Generating combined circle triangle")
    generate_semicircle()
    generate_square()
