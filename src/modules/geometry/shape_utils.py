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


# ---------------------------------------------------------------------------- #
from stl import mesh
from scipy.spatial import Delaunay


def save_as_stl(geometry, stl_filename="output.stl"):
    """
    Generate an STL mesh from a Shapely Polygon using Delaunay triangulation.

    Parameters:
        geometry (Polygon): The Shapely Polygon to be converted to a mesh.
        stl_filename (str): The name of the output STL file (default: "output.stl").

    Returns:
        None

    Notes:
        - The input geometry must be a Shapely Polygon.
        - The output STL file will be saved in the current working directory.
    """
    # Check if the input geometry is a Shapely Polygon
    if not isinstance(geometry, Polygon):
        raise ValueError("The input geometry must be a Shapely Polygon.")

    # Extract the vertices from the geometry and add z=0 to each coordinate (converting to 3D)
    vertices = np.array([list(coord) + [0] for coord in geometry.exterior.coords])

    # Ensure that the edges are connected (no duplicate points)
    faces = []

    # Use Delaunay triangulation to triangulate the geometry
    delaunay = Delaunay(vertices[:, :2])  # Delaunay works only in 2D

    # Generate the faces from the Delaunay triangulation
    faces = delaunay.simplices

    # Create the STL mesh from the generated faces
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        mesh_data.vectors[i] = vertices[f]

    # Save the STL file
    mesh_data.save(stl_filename)
    print(f"STL saved: {stl_filename}")


# -------------------------------------------------------- #
# -------------------------------------------------------- #
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union


def merge_shapes(geometry1, geometry2):
    """
    Merge two geometric shapes into a single shape.

    This function takes two Shapely Polygons and merges them using a robust
    union operation. It handles cases where the geometries intersect or overlap.
    If the union results in a MultiPolygon, the largest polygon by area is chosen.

    Parameters:
        geometry1 (Polygon): The first geometry to merge.
        geometry2 (Polygon): The second geometry to merge.

    Returns:
        Polygon: A single merged Polygon.

    Raises:
        ValueError: If the result of the union is not a valid Polygon.
    """
    # Perform a robust union of the two geometries
    merged_geometry = unary_union([geometry1, geometry2])

    # If the result is a MultiPolygon, select the largest polygon by area
    if isinstance(merged_geometry, MultiPolygon):
        merged_geometry = max(merged_geometry.geoms, key=lambda p: p.area)

    # Ensure the result is a valid Polygon
    if not isinstance(merged_geometry, Polygon):
        raise ValueError("The merged geometries did not result in a valid Polygon.")

    return merged_geometry


# -------------------------------------------------------- #
#                        SAVE AS PNG                       #
# -------------------------------------------------------- #


# -------------------------------------------------------- #
#                     GENERATE FILENAME                    #
# -------------------------------------------------------- #

# Define directories
STL_DIR = "geometries/obstacles/stl"
PNG_DIR = "geometries/obstacles/png"

# Ensure directories exist
os.makedirs(STL_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)


def save_files(shape, label, left_stretch, right_stretch, angle):

    name = f"{label}_lstretch{int(left_stretch*100):03d}_rstretch{int(right_stretch*100):03d}_rot{int(angle):03d}"

    stl_name = os.path.join(STL_DIR, f"{name}" + ".stl")

    save_as_stl(shape, stl_name)

    png_name = os.path.join(PNG_DIR, f"{name}" + ".png")

    save_as_png(shape, png_name)


# -------------------------------------------------------- #
#                        SAVE AS PNG                       #
# -------------------------------------------------------- #

from PIL import Image, ImageDraw
from shapely.geometry import Polygon


def save_as_png(polygon_object, png_name):
    # Obter as coordenadas do polígono
    x, y = polygon_object.exterior.xy
    coords = list(zip(x, y))  # Criar lista de coordenadas (x, y)

    # Calcular os limites do polígono (bounding box)
    min_x = min(coord[0] for coord in coords)
    max_x = max(coord[0] for coord in coords)
    min_y = min(coord[1] for coord in coords)
    max_y = max(coord[1] for coord in coords)

    width = max_x - min_x
    height = max_y - min_y

    # Calcular o tamanho da imagem com base nos limites (1.1 vezes width e height)
    img_width = int(1.2 * width * 100)  # Aumenta 10% para dar margem
    img_height = int(1.2 * height * 100)

    # Criar uma imagem em branco
    img = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(img)

    # Calcular o centroide do polígono
    centroid_x, centroid_y = polygon_object.centroid.x, polygon_object.centroid.y

    # Ajustar as coordenadas do polígono para caber na imagem com a escala
    scale = 100  # Fator de escala para ajustar o polígono à imagem
    scaled_coords = [
        (
            int((x - (min_x + max_x) / 2) * scale + img_width / 2),
            int((y - (min_y + max_y) / 2) * scale + img_height / 2),
        )
        for x, y in coords
    ]

    # Desenhar o polígono centralizado
    draw.polygon(scaled_coords, fill="black")

    # Salvar a imagem como PNG
    img.save(png_name)

    print(f"Imagem salva: {png_name}")
