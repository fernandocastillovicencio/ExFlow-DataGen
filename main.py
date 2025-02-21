import os
import shutil


def remove_conteudo_pasta(pasta):
    if os.path.exists(pasta):  # Check if the directory exists
        for f in os.listdir(pasta):
            file_path = os.path.join(pasta, f)  # Get full path of the file/folder

            if os.path.isdir(file_path):  # Check if it's a directory
                shutil.rmtree(file_path)  # Remove the directory and its contents
            elif os.path.isfile(file_path):  # Check if it's a file
                os.remove(file_path)  # Remove the file
            else:
                print(f"Skipping non-file and non-directory: {file_path}")
    else:
        print(f"Directory '{pasta}' not found.")


remove_conteudo_pasta("geometries/domain")
remove_conteudo_pasta("geometries/merged")


os.system("PYTHONPATH=src salome -t src/modules/geometry/domain.py")
os.system("salome killall")
