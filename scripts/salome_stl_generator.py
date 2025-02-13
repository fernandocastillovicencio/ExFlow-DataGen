import os
import random
import salome
import logging

# Initialize Salome and the geometry builder
salome.salome_init()
import GEOM
from salome.geom import geomBuilder

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/salome_stl_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SalomeSTLGenerator")

# Create geometry builder instance
geompy = geomBuilder.New()

# Domain parameters
domain_width = 260
domain_height = 120
domain_thickness = 10

# Output directory
output_dir = "cases/geometries"
os.makedirs(output_dir, exist_ok=True)

O = geompy.MakeVertex(0, 0, 0)

# Define number of obstacles
N = 981

# Geometric shapes available
shapes = ["circle", "square", "triangle_forward", "triangle_inverted", "rhombus"]

# Set to store unique obstacle parameters
unique_geometries = set()

# Function to create obstacle folder
def create_obstacle_folder(index):
    folder_path = os.path.join(output_dir, f"geom_{index:04d}")
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# Function to generate STL filename
def generate_filename(folder, index, part):
    return os.path.join(folder, f"geom_{index:04d}-{part}.stl")

# Generate obstacles
generated_count = 0
attempts = 0

while generated_count < N:
    attempts += 1
    selected_shape = random.choice(shapes)
    logger.info(f"Attempt {attempts}: Generating shape {generated_count+1}/{N}: {selected_shape}")

    back = geompy.MakeFaceHW(domain_width, domain_height, 1)
    geompy.TranslateDXDYDZ(back, 0, 0, -domain_thickness / 2)
    front = geompy.MakeTranslation(back, 0, 0, domain_thickness)

    inlet = geompy.MakeFaceHW(domain_thickness, domain_height, 2)
    geompy.TranslateDXDYDZ(inlet, -domain_width / 2, 0, 0)
    outlet = geompy.MakeTranslation(inlet, domain_width, 0, 0)

    upper = geompy.MakeFaceHW(domain_thickness, domain_width, 3)
    geompy.TranslateDXDYDZ(upper, 0, domain_height / 2, 0)
    lower = geompy.MakeTranslation(upper, 0, -domain_height, 0)

    length = domain_width / 6
    for part in [back, front, inlet, outlet, upper, lower]:
        geompy.TranslateDXDYDZ(part, length, 0, 0)

    base_wire = None

    if selected_shape == "circle":
        radius = random.uniform(5, 12)
        base_wire = geompy.MakeCircle(None, None, radius)
        unique_geometries.add((selected_shape, round(radius, 2)))

    elif selected_shape == "square":
        side = random.uniform(15, 35)
        sk = geompy.Sketcher2D()
        marker = geompy.MakeMarker(0, 0, 0, 0.001, 0, 0, 0, 0.001, 0)
        sk.addPoint(-side / 2, -side / 2)
        sk.addSegmentRelative(side, 0)
        sk.addSegmentRelative(0, side)
        sk.addSegmentRelative(-side, 0)
        sk.close()
        base_wire = sk.wire(marker)
        unique_geometries.add((selected_shape, round(side, 2)))

    elif selected_shape in ["triangle_forward", "triangle_inverted"]:
        base = random.uniform(10, 25)
        height = random.uniform(10, 25)
        sk = geompy.Sketcher2D()
        marker = geompy.MakeMarker(0, 0, 0, 0.001, 0, 0, 0, 0.001, 0)
        if selected_shape == "triangle_forward":
            sk.addPoint(base / 2, -height / 2)
            sk.addSegmentRelative(0, height)
            sk.addSegmentAbsolute(-base / 2, -height / 2)
        else:
            sk.addPoint(base / 2, height / 2)
            sk.addSegmentRelative(0, -height)
            sk.addSegmentAbsolute(-base / 2, height / 2)
        sk.close()
        base_wire = sk.wire(marker)
        unique_geometries.add((selected_shape, round(base, 2), round(height, 2)))

    elif selected_shape == "rhombus":
        base = random.uniform(10, 25)
        height = random.uniform(10, 25)
        offset = random.uniform(5, 15)
        sk = geompy.Sketcher2D()
        marker = geompy.MakeMarker(0, 0, 0, 0.001, 0, 0, 0, 0.001, 0)
        sk.addPoint(-base / 2, -height / 2)
        sk.addSegmentRelative(base, 0)
        sk.addSegmentRelative(offset, height)
        sk.addSegmentAbsolute(-base / 2 + offset, height / 2)
        sk.close()
        base_wire = sk.wire(marker)
        unique_geometries.add((selected_shape, round(base, 2), round(height, 2), round(offset, 2)))

    if base_wire:
        geompy.TranslateDXDYDZ(base_wire, 0, 0, -domain_thickness / 2)

        # Adição das faces back/front corrigidas
        face_obstacle_back = geompy.MakeFaceWires([base_wire], 1)
        face_obstacle_front = geompy.MakeTranslation(face_obstacle_back, 0, 0, domain_thickness)

        back = geompy.MakeCutList(back, [face_obstacle_back], True)
        front = geompy.MakeCutList(front, [face_obstacle_front], True)

        obstacle = geompy.MakePrismVecH(base_wire, geompy.MakeVectorDXDYDZ(0, 0, 1), domain_thickness)

        folder_path = create_obstacle_folder(generated_count + 1)

        obstacle = geompy.MakeScaleTransform(obstacle, O, 0.001)
        inlet = geompy.MakeScaleTransform(inlet, O , 0.001)
        outlet = geompy.MakeScaleTransform(outlet, O , 0.001)
        upper = geompy.MakeScaleTransform(upper, O , 0.001)
        lower = geompy.MakeScaleTransform(lower, O , 0.001)
        front = geompy.MakeScaleTransform(front, O , 0.001)
        back = geompy.MakeScaleTransform(back, O , 0.001)

        geompy.ExportSTL(obstacle, generate_filename(folder_path, generated_count + 1, "obstacle"), True, 0.001, False)
        geompy.ExportSTL(inlet, generate_filename(folder_path, generated_count + 1, "inlet"), True, 0.001, False)
        geompy.ExportSTL(outlet, generate_filename(folder_path, generated_count + 1, "outlet"), True, 0.001, False)
        geompy.ExportSTL(upper, generate_filename(folder_path, generated_count + 1, "upper"), True, 0.001, False)
        geompy.ExportSTL(lower, generate_filename(folder_path, generated_count + 1, "lower"), True, 0.001, False)
        geompy.ExportSTL(front, generate_filename(folder_path, generated_count + 1, "front"), True, 0.001, False)
        geompy.ExportSTL(back, generate_filename(folder_path, generated_count + 1, "back"), True, 0.001, False)

        generated_count += 1
        logger.info(f"Generated {generated_count}/{N} obstacles.")

logger.info("Successfully generated 981 unique obstacles.")
