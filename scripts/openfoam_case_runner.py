import logging
from modules.geometry_handler import get_geometry_folders, merge_stl_files
from modules.case_initializer import create_case_folders, copy_template

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/openfoam_case_runner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("OpenFOAMCaseRunner")

# Main execution
if __name__ == "__main__":
    geometries = get_geometry_folders()

    for idx, geom in enumerate(geometries[:2], start=1):  # Testing with 2 cases
        case_folder = create_case_folders(idx)
        geom_folder = f"cases/geometries/{geom}"

        # Copy ONLY meshing templates (cfMesh)
        copy_template(case_folder, "system.cfmesh", "system")
        copy_template(case_folder, "constant.cfmesh", "constant")

        # Merge STL files
        merge_stl_files(idx, geom_folder)
