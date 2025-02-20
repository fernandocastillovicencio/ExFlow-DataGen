import os
from stl import mesh
import numpy as np

import os
from stl import mesh
import numpy as np


def calculate_centroid_from_faces(stl_file):
    """
    Calcula o centroide ponderado de um objeto 3D a partir das faces do STL.

    Parameters:
        stl_file (str): Caminho para o arquivo STL.

    Returns:
        np.ndarray: O centroide ponderado calculado a partir das faces.
    """
    stl_mesh = mesh.Mesh.from_file(stl_file)
    centroid = np.zeros(3)
    total_area = 0.0

    for i in range(len(stl_mesh.vectors)):
        v0, v1, v2 = stl_mesh.vectors[i]

        vec1 = v1 - v0
        vec2 = v2 - v0

        area = np.linalg.norm(np.cross(vec1, vec2)) / 2.0
        face_centroid = (v0 + v1 + v2) / 3.0

        centroid += face_centroid * area
        total_area += area

    centroid /= total_area
    return centroid


def move_to_origin(vertices, centroid):
    """
    Move o objeto para que o centroide coincida com (0, 0).

    Parameters:
        vertices (numpy array): Os vértices do objeto STL.
        centroid (numpy array): O centroide do objeto.

    Returns:
        numpy array: Vértices movidos com o centroide em (0,0).
    """
    return vertices - centroid


def scale_stl(vertices, scale_factor):
    """
    Aplica a escala ao STL mantendo o centroide em (0,0).

    Parameters:
        vertices (numpy array): Vértices do objeto STL.
        scale_factor (float): Fator de escala.

    Returns:
        numpy array: Vértices escalados.
    """
    return vertices * scale_factor


def calculate_new_centroid(vertices):
    """
    Calcula o novo centroide do objeto após a transformação (escala).

    Parameters:
        vertices (numpy array): Vértices transformados do objeto.

    Returns:
        np.ndarray: O novo centroide do objeto.
    """
    new_centroid = np.mean(vertices, axis=0)  # Cálculo da média dos vértices
    return new_centroid


def calculate_new_bounding_box(vertices):
    """
    Calcula o novo bounding box do objeto após a transformação (escala).

    Parameters:
        vertices (numpy array): Vértices transformados do objeto.

    Returns:
        tuple: O novo bounding box (min_coords, max_coords).
    """
    min_coords = np.min(vertices, axis=0)
    max_coords = np.max(vertices, axis=0)
    return min_coords, max_coords


def save_scaled_stl(vertices, original_stl, output_directory, scale_factor):
    """
    Salva um novo arquivo STL após a aplicação da escala.

    Parameters:
        vertices (numpy array): Vértices escalados.
        original_stl (str): Caminho do arquivo STL original.
        output_directory (str): Diretório onde salvar o STL escalado.
        scale_factor (float): Fator de escala aplicado.

    Returns:
        None
    """
    num_faces = vertices.shape[0] // 3
    new_mesh = mesh.Mesh(np.zeros(num_faces, dtype=mesh.Mesh.dtype))

    for i in range(num_faces):
        new_mesh.vectors[i] = vertices[i * 3 : (i + 1) * 3]

    base_name = os.path.basename(original_stl).replace(".stl", "")
    output_file = os.path.join(output_directory, f"{base_name}.stl")

    new_mesh.save(output_file)
    print(f"STL escalado salvo em: {output_file}")


def process_and_scale_stl(directory, domain_width=260, domain_height=120):
    """
    Processa os dois primeiros arquivos STL no diretório, calcula o bounding box, move o objeto,
    aplica a escala com base no domínio e salva o novo STL, calculando o novo centroide e bounding box.

    Parameters:
        directory (str): Caminho do diretório onde os arquivos STL estão armazenados.
        domain_width (float): Largura do domínio (padrão 260).
        domain_height (float): Altura do domínio (padrão 120).

    Returns:
        None
    """
    output_directory = "geometries/domain"
    os.makedirs(output_directory, exist_ok=True)

    # Obter os dois primeiros arquivos STL no diretório
    stl_files = [f for f in os.listdir(directory) if f.endswith(".stl")][:2]

    # Iterar apenas sobre os dois primeiros arquivos
    for filename in stl_files:
        file_path = os.path.join(directory, filename)

        # Calcular o centroide ponderado
        centroid = calculate_centroid_from_faces(file_path)

        # Carregar o arquivo STL
        stl_mesh = mesh.Mesh.from_file(file_path)
        vertices = stl_mesh.vectors.reshape(-1, 3)

        # Calcular o bounding box do objeto
        min_coords = np.min(vertices, axis=0)
        max_coords = np.max(vertices, axis=0)

        # Mover o objeto para o centroide
        moved_vertices = move_to_origin(vertices, centroid)

        # Calcular fator de escala
        scalex = domain_width / (max_coords[0] - min_coords[0]) / 13
        scaley = domain_height / (max_coords[1] - min_coords[1]) / 5
        scale = min(scalex, scaley)

        # Aplicar escala
        scaled_vertices = scale_stl(moved_vertices, scale)

        # Calcular o novo centroide e o novo bounding box após a transformação
        new_centroid = calculate_new_centroid(scaled_vertices)
        new_min_coords, new_max_coords = calculate_new_bounding_box(scaled_vertices)

        # Salvar STL escalado
        save_scaled_stl(scaled_vertices, file_path, output_directory, scale)

        # Mostrar resultados
        print(f"\nProcessado: {filename}")
        print(
            f"Bounding Box Original -> Width: {max_coords[0] - min_coords[0]}, Height: {max_coords[1] - min_coords[1]}"
        )
        print(f"Escala aplicada -> ScaleX: {scalex}, ScaleY: {scaley}, Final: {scale}")
        print(f"Centroide Original: {centroid}")
        print(f"Novo Centroide: {new_centroid}")
        print(
            f"Novo Bounding Box -> Width: {new_max_coords[0] - new_min_coords[0]}, Height: {new_max_coords[1] - new_min_coords[1]}"
        )
        print("-" * 40)


# Exemplo de uso
stl_directory = "geometries/obstacles/stl"  # Altere para o caminho correto
process_and_scale_stl(stl_directory)
