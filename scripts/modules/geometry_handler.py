import os
import re
import logging

logger = logging.getLogger("OpenFOAMCaseRunner")

GEOMETRY_DIR = "cases/geometries/"

def get_geometry_folders():
    """ Scan the geometries directory and return a list of valid geometry folders. """
    if not os.path.exists(GEOMETRY_DIR):
        logger.error(f"Geometry directory {GEOMETRY_DIR} not found!")
        return []

    geometry_folders = sorted([
        folder for folder in os.listdir(GEOMETRY_DIR)
        if os.path.isdir(os.path.join(GEOMETRY_DIR, folder)) and folder.startswith("geom_")
    ])

    logger.info(f"Found {len(geometry_folders)} geometry folders.")
    return geometry_folders

def merge_stl_files(case_id, geom_folder):
    """ Merge STL files into a single geom.stl file for OpenFOAM. """
    case_folder = f"cases/cases_run/case_{case_id:04d}/constant/triSurface"
    os.makedirs(case_folder, exist_ok=True)
    output_stl = os.path.join(case_folder, "geom.stl")

    stl_files = sorted([f for f in os.listdir(geom_folder) if f.endswith(".stl")])

    with open(output_stl, "w") as outfile:
        for stl_file in stl_files:
            surface_name = re.sub(r'^\d+-', '', os.path.splitext(stl_file)[0].split("_")[-1])
            with open(os.path.join(geom_folder, stl_file), "r") as infile:
                lines = infile.readlines()
                outfile.write(f"solid {surface_name}\n")
                copying = False
                for line in lines:
                    if line.strip().startswith("solid"):
                        copying = True
                    elif line.strip().startswith("endsolid"):
                        copying = False
                    elif copying:
                        outfile.write(line)
                outfile.write(f"endsolid {surface_name}\n\n")

    logger.info(f"Merged STL saved: {output_stl}")
