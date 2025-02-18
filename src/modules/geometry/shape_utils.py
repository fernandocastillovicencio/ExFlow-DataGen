"""
Utility functions for saving geometric shapes as STL and PNG files.

This module provides functions to compute the image size based on the STL bounding box,
and to save geometric shapes as STL and PNG files. The module ensures that the necessary
directories for saving images and STL files exist.

Functions:
- compute_image_size(vertices, target_height=320, margin_factor=0.05): Computes the image size
  based on the STL bounding box.
- save_as_stl(vertices, faces, filename): Saves the given vertices and faces as an STL file.
- save_as_png(vertices, filename): Saves the given vertices as a black-and-white PNG image.
"""

import os
import numpy as np
import cv2
import trimesh
import shapely.ops as so
import shapely.geometry as sg

# Define directories
IMAGE_DIR = "geometries/obstacles/images"
STL_DIR = "geometries/obstacles/stl"

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(STL_DIR, exist_ok=True)


def compute_image_size(vertices, target_height=320, margin_factor=0.05):
    """
    Compute the image size based on STL bounding box.

    Given the target image height, this function computes the image width, pixels per meter,
    and the minimum x and y values for the image such that the STL shape fits within the
    image with a specified margin.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        target_height (int): Desired image height in pixels.
        margin_factor (float): Percentage of margin to add around the shape.

    Returns:
        tuple: (image_width, image_height, pixels_per_meter, min_x, min_y)

    Notes:
        - The margin is added to the width and height of the STL shape.
        - The image width and height are computed based on the target height and the width
          and height of the STL shape with the added margin.
        - The pixels per meter is computed as the target height divided by the height of
          the STL shape with the added margin.
        - The min_x and min_y values are the minimum x and y values of the STL shape with
          the added margin.
    """
    # Compute the bounding box of the STL shape
    min_x, min_y = np.min(vertices[:, :2], axis=0)
    max_x, max_y = np.max(vertices[:, :2], axis=0)

    # Compute the width and height of the STL shape
    width_m = max_x - min_x
    height_m = max_y - min_y

    # Compute the margin to add to the width and height
    margin_x = width_m * margin_factor
    margin_y = height_m * margin_factor

    # Add the margin to the width and height
    min_x -= margin_x
    max_x += margin_x
    min_y -= margin_y
    max_y += margin_y

    # Compute the width and height of the image
    width_m = max_x - min_x
    height_m = max_y - min_y

    # Compute the number of pixels per meter
    pixels_per_meter = target_height / height_m

    # Compute the image width and height
    image_width = int(width_m * pixels_per_meter)
    image_height = target_height

    # Return the computed values
    return image_width, image_height, pixels_per_meter, min_x, min_y


def save_as_stl(vertices, faces, filename):
    """
    Save the given vertices and faces as an STL file.

    Parameters:
        vertices (np.ndarray): Array of vertices (N,3) defining the shape.
        faces (np.ndarray): Array of indices forming triangular faces.
        filename (str): Base name for the output STL file.

    Notes:
        - The file is saved in the predefined STL directory.
    """
    # Construct the full path for the STL file
    # The filename parameter is used as the base name, and the STL
    # extension is added automatically.
    stl_path = os.path.join(STL_DIR, f"{filename}.stl")

    # Create a 3D mesh object from the vertices and faces
    # The trimesh library is used to create a mesh object from the
    # given vertices and faces.
    shape_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Export the mesh to an STL file at the specified path
    # The export method is used to save the mesh as an STL file.
    shape_mesh.export(stl_path)

    # Print confirmation of the saved file
    # The saved file path is printed to the console.
    print(f"STL saved: {stl_path}")


def save_as_png(vertices, filename):
    """
    Save the given vertices as a black-and-white PNG image.

    The image is created by transforming the STL shape to a 2D image with the specified
    target height. The STL shape is centered within the image and the image is padded with
    a margin to ensure the shape fits within the image.

    Parameters:
        vertices (np.ndarray): Array of vertices (N,3) defining the shape.
        filename (str): Base name for the output PNG file.

    Notes:
        - The file is saved in the predefined image directory.
    """
    # Compute the image size
    image_width, image_height, pixels_per_meter, min_x, min_y = compute_image_size(
        vertices
    )

    # Create a white image with the computed size
    image = np.ones((image_height, image_width), dtype=np.uint8) * 255

    # Transform the vertices to pixel coordinates
    # The x and y coordinates are computed by subtracting the minimum x and y values
    # from the vertices, and then multiplying by the pixels per meter.
    pixel_x = ((vertices[:, 0] - min_x) * pixels_per_meter).astype(int)
    pixel_y = ((vertices[:, 1] - min_y) * pixels_per_meter).astype(int)

    # Create a list of points for the polygon
    # The points are created by zipping together the x and y coordinates.
    points = np.array(list(zip(pixel_x, pixel_y)), dtype=np.int32)

    # Fill the polygon with black
    # The fillPoly function is used to fill the polygon with black.
    cv2.fillPoly(image, [points], color=0)

    # Construct the full path for the PNG file
    # The filename parameter is used as the base name, and the PNG extension is added
    # automatically.
    image_path = os.path.join(IMAGE_DIR, f"{filename}.png")
    # Save the image to the specified path
    cv2.imwrite(image_path, image)
    # Print confirmation of the saved file
    print(f"Image saved: {image_path}")


# ---------------------------------------------------------------------------- #


def create_mesh_from_shape(geometry, num_edges=10):
    """
    Cria uma malha 3D a partir de uma figura 2D do Shapely e retorna a malha do Trimesh.
    A malha gerada estará no plano XY (com Z=0), com cada forma dividida em `num_edges` arestas.

    Parameters:
    - geometry: A figura 2D do Shapely para a qual queremos criar a malha.
    - num_edges: O número de segmentos desejados para a borda da forma. Padrão é 10.

    Returns:
    - trimesh.Trimesh: A malha 3D gerada.
    """
    # Se a geometria for um quadrado, use a função modificada
    if (
        isinstance(geometry, sg.Polygon)
        and geometry.is_valid
        and len(list(geometry.exterior.coords)) == 5
    ):  # quadrado fechado com 4 vértices
        # Garantir que seja tratado com 10 segmentos
        triangles = so.triangulate(geometry)
    else:
        # Para formas gerais, aplicamos a triangulação padrão
        triangles = so.triangulate(geometry)

    vertices_list = []
    faces_list = []

    # Para cada triângulo gerado pela triangulação
    for triangle in triangles:
        coords = list(triangle.exterior.coords)[
            :-1
        ]  # Remove o ponto duplicado no final
        idx = len(vertices_list)  # Índice base para os vértices desse triângulo
        vertices_list.extend(
            [(x, y, 0) for x, y in coords]
        )  # Adiciona os vértices com z=0
        faces_list.append([idx, idx + 1, idx + 2])  # Adiciona a face como triângulo

    # Converter listas para arrays numpy
    vertices = np.array(vertices_list)
    faces = np.array(faces_list)

    # Criar a malha Trimesh
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    return mesh


# ---------------------------------------------------------------------------- #


from shapely.geometry import Polygon
import numpy as np
from stl import mesh
from scipy.spatial import Delaunay


def generate_mesh_from_polygon(geometry, stl_filename="output.stl"):
    """
    Gera um mesh STL a partir de uma geometria do Shapely (Polygon) usando Triangulação de Delaunay.

    Parameters:
        geometry (Polygon): A geometria do Shapely a ser convertida para um mesh.
        stl_filename (str): Nome do arquivo STL de saída (default: "output.stl").
    """
    if not isinstance(geometry, Polygon):
        raise ValueError("A geometria deve ser um Polygon do Shapely.")

    # Extraindo os vértices da geometria e adicionando z=0 para cada coordenada (convertendo para 3D)
    vertices = np.array([list(coord) + [0] for coord in geometry.exterior.coords])

    # Garantir que as arestas sejam conectadas (não há pontos duplicados)
    faces = []

    # Usando Delaunay para triangulação da geometria
    delaunay = Delaunay(vertices[:, :2])  # Delaunay trabalha apenas no plano 2D

    # Gerar as faces a partir da triangulação de Delaunay
    faces = delaunay.simplices

    # Criando o mesh STL a partir das faces geradas pela triangulação de Delaunay
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        mesh_data.vectors[i] = vertices[f]

    # Salvando o arquivo STL
    mesh_data.save(stl_filename)
    print(f"STL saved: {stl_filename}")
