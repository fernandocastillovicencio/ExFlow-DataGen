import os
import shutil

from modules.cfmesh4meshing.meshing import meshing

# -------------------------------------------------------- #
#                         FUNCTIONS                        #
# -------------------------------------------------------- #
BASE_DIR = os.getcwd()


def remove_folder_content(folder):
    if os.path.exists(folder):  # Check if the directory exists
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)  # Get full path of the file/folder

            if os.path.isdir(file_path):  # Check if it's a directory
                shutil.rmtree(file_path)  # Remove the directory and its contents
            elif os.path.isfile(file_path):  # Check if it's a file
                os.remove(file_path)  # Remove the file
            else:
                print(f"Skipping non-file and non-directory: {file_path}")
    else:
        print(f"Directory '{folder}' not found.")


# -------------------------------------------------------- #
#                         GEOMETRY                         #
# -------------------------------------------------------- #
# remove_folder_content("geometries/domain")
# remove_folder_content("geometries/merged")
# os.system("PYTHONPATH=src salome -t src/modules/geometry/domain.py")

# -------------------------------------------------------- #
#                          MESHING                         #
# -------------------------------------------------------- #
# remove_folder_content("meshes/")
# remove_folder_content("cases/")
meshing()

# -------------------------------------------------------- #
#                         FINISHING                        #
# -------------------------------------------------------- #
# os.system("salome killall")
