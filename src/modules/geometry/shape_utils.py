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

# Define directories
IMAGE_DIR = "geometries/obstacles/images"
STL_DIR = "geometries/obstacles/stl"

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(STL_DIR, exist_ok=True)


# ---------------------------------------------------------------------------- #
from stl import mesh
from scipy.spatial import Delaunay


def generate_mesh_from_polygon(geometry, stl_filename="output.stl"):
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
