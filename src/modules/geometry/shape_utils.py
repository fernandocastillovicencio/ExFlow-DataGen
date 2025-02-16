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

    Given the target image height, this function computes the image width, pixels per meter,
    and the minimum x and y values for the image such that the STL shape fits within the
    image with a specified margin.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        target_height (int): Desired image height in pixels.
        margin_factor (float): Percentage of margin to add around the shape.

    Returns:
        tuple: (image_width, image_height, pixels_per_meter, min_x, min_y)
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
    stl_path = os.path.join(STL_DIR, f"{filename}.stl")

    # Create a 3D mesh object from the vertices and faces
    shape_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Export the mesh to an STL file at the specified path
    shape_mesh.export(stl_path)

    # Print confirmation of the saved file
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
    image_width, image_height, pixels_per_meter, min_x, min_y = compute_image_size(
        vertices
    )

    # Create a white image with the computed size
    image = np.ones((image_height, image_width), dtype=np.uint8) * 255

    # Transform the vertices to pixel coordinates
    pixel_x = ((vertices[:, 0] - min_x) * pixels_per_meter).astype(int)
    pixel_y = ((vertices[:, 1] - min_y) * pixels_per_meter).astype(int)

    # Create a list of points for the polygon
    points = np.array(list(zip(pixel_x, pixel_y)), dtype=np.int32)

    # Fill the polygon with black
    cv2.fillPoly(image, [points], color=0)

    # Construct the full path for the PNG file
    image_path = os.path.join(IMAGE_DIR, f"{filename}.png")
    cv2.imwrite(image_path, image)
    print(f"Image saved: {image_path}")
