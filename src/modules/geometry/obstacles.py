"""
This module handles the generation and saving of geometric obstacle shapes, including semicircles.

Functions:
- compute_image_size(vertices, target_height=320, margin_factor=0.05): Computes the image size based on the STL bounding box.
- generate_semicircle(filename="semicircle"): Generates a semicircle with a straight edge and saves it as an STL and PNG file.

The module ensures that the necessary directories for saving images and STL files exist.
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

    The image size is computed such that the STL shape fits within the image
    with a specified margin. The margin is added to the width and height of the
    STL shape, and the image dimensions are computed based on the target height
    and the width and height of the STL shape with the added margin.

    Parameters:
        vertices (np.ndarray): Numpy array of shape (N,3) with STL vertices.
        target_height (int): Desired image height in pixels.
        margin_factor (float): Percentage of margin to add around the shape.

    Returns:
        tuple: (image_width, image_height) in pixels.
    """
    # Compute the bounding box of the STL shape
    min_x, min_y = np.min(vertices[:, :2], axis=0)
    max_x, max_y = np.max(vertices[:, :2], axis=0)

    # Compute the width and height of the STL shape
    width_m = max_x - min_x
    height_m = max_y - min_y

    # Compute the margin to add to the width and height
    width_m *= 1 + 2 * margin_factor
    height_m *= 1 + 2 * margin_factor

    # Compute the number of pixels per meter
    pixels_per_meter = target_height / height_m

    # Compute the image width and height
    image_width = int(width_m * pixels_per_meter)
    image_height = target_height

    return image_width, image_height


def generate_semicircle(filename="semicircle"):
    """
    Generate a semicircle (half-circle) with a straight edge and save it as an STL and PNG.

    Parameters:
        filename (str): The base filename for the STL and PNG files.

    Notes:
        - The semicircle is centered at (0,0) with radius 1.
        - The curved edge passes through (0,1), (-1,0), (0,-1).
        - The straight edge is between (0,1) and (0,-1).
    """

    # Define semicircle geometry in meters
    radius_m = 1.0
    num_points = 50  # Number of points for smooth curvature

    # Compute semicircle points (left side)
    theta = np.linspace(np.pi / 2, 3 * np.pi / 2, num=num_points)
    x = radius_m * np.cos(theta)
    y = radius_m * np.sin(theta)
    z = np.zeros_like(x)  # Keep it 2D

    # Define straight edge points (right side)
    x_straight = np.array([0, 0])
    y_straight = np.array([1, -1])
    z_straight = np.zeros_like(x_straight)

    # Combine curved and straight edges
    vertices = np.column_stack(
        (
            np.concatenate([x, x_straight]),
            np.concatenate([y, y_straight]),
            np.concatenate([z, z_straight]),
        )
    )

    # Create faces (triangulation)
    faces = [[i, i + 1, len(vertices) - 1] for i in range(len(vertices) - 2)]
    faces.append([len(vertices) - 2, 0, len(vertices) - 1])  # Close the shape

    # Create STL mesh
    semicircle_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Save STL
    stl_path = os.path.join(STL_DIR, f"{filename}.stl")
    semicircle_mesh.export(stl_path)
    print(f"STL saved: {stl_path}")

    # Compute image size based on STL bounds
    image_width, image_height = compute_image_size(vertices)

    # Create a white background image
    image = np.ones((image_height, image_width), dtype=np.uint8) * 255

    # Convert STL bounds to pixel space
    pixels_per_meter = image_height / (2.2)
    center = (image_width // 2, image_height // 2)

    # Convert real-world coordinates to pixels
    pixel_x = (x * pixels_per_meter + center[0]).astype(int)
    pixel_y = (y * pixels_per_meter + center[1]).astype(int)

    pixel_x_straight = (x_straight * pixels_per_meter + center[0]).astype(int)
    pixel_y_straight = (y_straight * pixels_per_meter + center[1]).astype(int)

    # Draw the curved part of the semicircle
    points = np.array(list(zip(pixel_x, pixel_y)), dtype=np.int32)
    cv2.polylines(image, [points], isClosed=False, color=0, thickness=2)

    # Draw the straight edge
    straight_points = np.array(
        list(zip(pixel_x_straight, pixel_y_straight)), dtype=np.int32
    )
    cv2.line(
        image,
        tuple(straight_points[0]),
        tuple(straight_points[1]),
        color=0,
        thickness=2,
    )

    # Fill the semicircle
    cv2.fillPoly(image, [np.vstack([points, straight_points[::-1]])], color=0)

    # Save PNG
    image_path = os.path.join(IMAGE_DIR, f"{filename}.png")
    cv2.imwrite(image_path, image)
    print(f"Image saved: {image_path}")


# If executed directly, generate a semicircle
if __name__ == "__main__":
    generate_semicircle()
