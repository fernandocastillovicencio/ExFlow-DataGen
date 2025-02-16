# src/modules/geometry/shape_utils.py
"""
Utility functions for saving shapes as STL and PNG.
"""

import os
import numpy as np
import cv2
import trimesh

# Define directories
IMAGE_DIR = "geometries/obstacles/images"
STL_DIR = "geometries/obstacles/stl"

# Ensure directories exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(STL_DIR, exist_ok=True)

def compute_image_size(vertices, target_height=320, margin_factor=0.05):
    """
    Compute the image size based on STL bounding box.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        target_height (int): Desired image height in pixels.
        margin_factor (float): Percentage of margin to add around the shape.

    Returns:
        tuple: (image_width, image_height, pixels_per_meter, min_x, min_y)
    """
    min_x, min_y = np.min(vertices[:, :2], axis=0)
    max_x, max_y = np.max(vertices[:, :2], axis=0)

    width_m = max_x - min_x
    height_m = max_y - min_y

    margin_x = width_m * margin_factor
    margin_y = height_m * margin_factor

    min_x -= margin_x
    max_x += margin_x
    min_y -= margin_y
    max_y += margin_y

    width_m = max_x - min_x
    height_m = max_y - min_y

    pixels_per_meter = target_height / height_m
    image_width = int(width_m * pixels_per_meter)
    image_height = target_height

    return image_width, image_height, pixels_per_meter, min_x, min_y

def save_as_stl(vertices, faces, filename):
    """
    Save the given vertices and faces as an STL file.
    """
    stl_path = os.path.join(STL_DIR, f"{filename}.stl")
    shape_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    shape_mesh.export(stl_path)
    print(f"STL saved: {stl_path}")

def save_as_png(vertices, filename):
    """
    Save the given vertices as a black-and-white PNG file.
    """
    image_width, image_height, pixels_per_meter, min_x, min_y = compute_image_size(vertices)

    image = np.ones((image_height, image_width), dtype=np.uint8) * 255

    pixel_x = ((vertices[:, 0] - min_x) * pixels_per_meter).astype(int)
    pixel_y = ((vertices[:, 1] - min_y) * pixels_per_meter).astype(int)

    points = np.array(list(zip(pixel_x, pixel_y)), dtype=np.int32)
    cv2.fillPoly(image, [points], color=0)

    image_path = os.path.join(IMAGE_DIR, f"{filename}.png")
    cv2.imwrite(image_path, image)
    print(f"Image saved: {image_path}")
