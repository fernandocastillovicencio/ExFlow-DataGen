import numpy as np
import cv2
import os
import glob

# Image parameters
IMAGE_SIZE = (256, 256)
CENTER = (IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2)
OUTPUT_FOLDER = "geometries/obstacles/images"  # Path to the image folder

# Create the output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Remove all files in the output folder
files = glob.glob(f"{OUTPUT_FOLDER}/*")
for f in files:
    os.remove(f)

def draw_circle(img):
    """Draws a circle."""
    radius = IMAGE_SIZE[0] // 5
    cv2.circle(img, CENTER, radius, (0, 0, 0), -1)
    return (2 * radius, 2 * radius)

def draw_ellipse(img):
    """Draws an ellipse."""
    size = IMAGE_SIZE[0] // 5
    cv2.ellipse(img, CENTER, (size, size // 2), 0, 0, 360, (0, 0, 0), -1)
    return (2 * size, size)

def draw_capsule(img):
    """Draws a capsule (rectangle with rounded edges) with the circular side on the left."""
    size = IMAGE_SIZE[0] // 6
    radius = size // 2
    # Draw the left circular side
    cv2.circle(img, (CENTER[0] - size, CENTER[1]), radius, (0, 0, 0), -1)
    # Draw the rectangle part
    cv2.rectangle(img, (CENTER[0] - size, CENTER[1] - radius), (CENTER[0] + size, CENTER[1] + radius), (0, 0, 0), -1)
    # Draw the right circular side
    cv2.circle(img, (CENTER[0] + size, CENTER[1]), radius, (0, 0, 0), -1)
    return (2 * size, 2 * radius)

def draw_semi_circle(img):
    """Draws a semi-circle with 45 degrees tilt over the center."""
    radius = IMAGE_SIZE[0] // 5
    # Angle of rotation: 45 degrees
    angle = 90

    # Draw the tilted semi-circle
    cv2.ellipse(img, 
                (CENTER[0], CENTER[1]),    # Center of the ellipse (center of the image)
                (radius, radius),          # Horizontal and vertical radii
                angle,                     # Rotation angle
                0, 180,                    # Start and end angles for the semi-circle
                (0, 0, 0),                 # Color of the semi-circle (black)
                -1)                        # Filled

    return (2 * radius, 2 * radius)  # Return the size of the semi-circle image

def draw_diamond(img):
    """Draws a diamond."""
    size = IMAGE_SIZE[0] // 5
    points = np.array([
        [CENTER[0], CENTER[1] - size],  # Top
        [CENTER[0] + size, CENTER[1]],  # Right
        [CENTER[0], CENTER[1] + size],  # Bottom
        [CENTER[0] - size, CENTER[1]]   # Left
    ])
    cv2.fillPoly(img, [points], (0, 0, 0))
    return (2 * size, 2 * size)

def draw_triangle(img):
    """Draws an equilateral triangle."""
    size = IMAGE_SIZE[0] // 5
    points = np.array([
        [CENTER[0], CENTER[1] - size],  # Top vertex
        [CENTER[0] - size, CENTER[1] + size],  # Bottom-left vertex
        [CENTER[0] + size, CENTER[1] + size]   # Bottom-right vertex
    ])
    cv2.fillPoly(img, [points], (0, 0, 0))
    return (2 * size, 2 * size)

def draw_pentagon(img):
    """Draws a regular pentagon."""
    size = IMAGE_SIZE[0] // 5
    # Calculate the vertices for a regular pentagon
    points = []
    for i in range(5):
        angle = 2 * np.pi * i / 5  # Angle between each vertex
        x = int(CENTER[0] + size * np.cos(angle))
        y = int(CENTER[1] + size * np.sin(angle))
        points.append([x, y])
    
    points = np.array(points)
    cv2.fillPoly(img, [points], (0, 0, 0))
    return (2 * size, 2 * size)

def draw_hexagon(img):
    """Draws a regular hexagon."""
    size = IMAGE_SIZE[0] // 5
    # Calculate the vertices for a regular hexagon
    points = []
    for i in range(6):
        angle = 2 * np.pi * i / 6  # Angle between each vertex
        x = int(CENTER[0] + size * np.cos(angle))
        y = int(CENTER[1] + size * np.sin(angle))
        points.append([x, y])
    
    points = np.array(points)
    cv2.fillPoly(img, [points], (0, 0, 0))
    return (2 * size, 2 * size)

# Create images in increasing complexity order
shapes = {
    "circle": draw_circle,
    "ellipse": draw_ellipse,
    "capsule": draw_capsule,
    "semi-circle": draw_semi_circle,
    "diamond": draw_diamond,
    "triangle": draw_triangle,
    "pentagon": draw_pentagon,
    "hexagon": draw_hexagon
}

for i, (name, draw_function) in enumerate(shapes.items()):
    img = np.ones((IMAGE_SIZE[0], IMAGE_SIZE[1]), dtype=np.uint8) * 255  # White background
    draw_function(img)  # Draw the shape
    cv2.imwrite(f"{OUTPUT_FOLDER}/{name}.png", img)  # Save the image

print("Images generated successfully in the 'images' folder.")
