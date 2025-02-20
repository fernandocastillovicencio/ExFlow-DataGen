import os
from stl import mesh
import numpy as np


def get_bounding_box(stl_file):
    """
    Lê o arquivo STL e calcula o bounding box.

    Parameters:
        stl_file (str): Caminho para o arquivo STL.

    Returns:
        tuple: Bounding box (min_x, max_x, min_y, max_y, min_z, max_z), centroid
    """
    # Carregar o arquivo STL
    stl_mesh = mesh.Mesh.from_file(stl_file)

    # Obter todos os vértices
    vertices = stl_mesh.vectors.reshape(-1, 3)

    # Calcular o bounding box
    min_coords = np.min(vertices, axis=0)
    max_coords = np.max(vertices, axis=0)

    # Calcular o centroide (média das coordenadas dos vértices)
    centroid = np.mean(vertices, axis=0)

    return (
        min_coords[0],
        max_coords[0],
        min_coords[1],
        max_coords[1],
        min_coords[2],
        max_coords[2],
        centroid,
    )


def move_to_centroid(vertices, centroid):
    """
    Move o objeto para que o centroide coincida com (0, 0).

    Parameters:
        vertices (numpy array): Os vértices do objeto STL.
        centroid (numpy array): O centroide do objeto.

    Returns:
        numpy array: Vértices movidos com o centroide em (0,0).
    """
    # Mover o objeto para que o centroide seja (0, 0)
    moved_vertices = vertices - centroid
    return moved_vertices


def process_stl_files(directory, domain_width=260, domain_height=120):
    """
    Processa todos os arquivos STL em um diretório, calcula o bounding box, move o objeto,
    e calcula os fatores de escala.

    Parameters:
        directory (str): Caminho do diretório onde os arquivos STL estão armazenados.
        domain_width (float): Largura do domínio (padrão 260).
        domain_height (float): Altura do domínio (padrão 120).

    Returns:
        None
    """
    # Iterar sobre os arquivos no diretório
    for filename in os.listdir(directory):
        if filename.endswith(".stl"):
            file_path = os.path.join(directory, filename)
            min_x, max_x, min_y, max_y, min_z, max_z, centroid = get_bounding_box(
                file_path
            )

            # Calcular as dimensões do objeto
            object_width = max_x - min_x
            object_height = max_y - min_y

            # Calcular a escala
            scalex = domain_width / object_width / 13
            scaley = domain_height / object_height / 13

            print(f"Bounding Box para {filename}:")
            print(f"Width: {object_width}")
            print(f"Height: {object_height}")
            print(f"scalex: {scalex}")
            print(f"scaley: {scaley}")

            # Mover o objeto para o centroide
            stl_mesh = mesh.Mesh.from_file(file_path)
            vertices = stl_mesh.vectors.reshape(-1, 3)
            moved_vertices = move_to_centroid(vertices, centroid)

            # Mostrar os novos vértices movidos
            print(f"Centroid original: {centroid}")
            print(f"Vértices movidos (apenas os primeiros 5): {moved_vertices[:5]}")
            print("-" * 40)


# Exemplo de uso
stl_directory = "geometries/obstacles/stl"  # Altere para o caminho correto
process_stl_files(stl_directory)
