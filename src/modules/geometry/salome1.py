import sys
import salome

salome.salome_init()
import salome_notebook

notebook = salome_notebook.NoteBook()
sys.path.insert(0, r"/home/fernando/workspace/phd/202502/openfoam_data")

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()


O = geompy.MakeVertex(0, 0, 0)


import os

os.system("pkill -9 -f SALOME")


# -------------------------------------------------------- #
def load_stl_and_show_bounding_box(directory="geometries/domain"):
    """
    Carrega todos os arquivos STL de uma pasta e exibe o bounding box de cada um deles.
    """
    # Obter a lista de arquivos STL na pasta
    stl_files = [f for f in os.listdir(directory) if f.endswith(".stl")]

    # Carregar cada arquivo STL
    for stl_file in stl_files:
        # Caminho completo do arquivo STL
        file_path = os.path.join(directory, stl_file)

        # Carregar o STL usando o módulo GEOM
        part = geompy.ImportSTL(file_path)

        # Calcular o bounding box da geometria carregada
        bounding_box = part.BoundingBox()

        # Exibir os limites do bounding box
        print(f"Bounding Box do arquivo {stl_file}:")
        print(f"  Min: {bounding_box[0]}, Max: {bounding_box[1]}")

        # Mostrar o bounding box no Salome
        geompy.addToStudy(part, f"STL: {stl_file}")

        # Exibir limites no Salome (caixas de limite)
        min_point = bounding_box[0]
        max_point = bounding_box[1]
        geompy.AddBoundingBox(min_point, max_point)


# Executar a função
load_stl_and_show_bounding_box()

# -------------------------------------------------------- #


if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()
