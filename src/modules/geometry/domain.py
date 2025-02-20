from shapely.geometry import Polygon
from stl import mesh
import numpy as np

# Passo 1: Criar o retângulo 2D com Shapely
# Coordenadas do retângulo
rectangle_coords = [(-60, -60), (200, -60), (200, 60), (-60, 60)]

# Criar o polígono 2D (retângulo)
rectangle = Polygon(rectangle_coords)

# Passo 2: Extrudar o retângulo para criar uma superfície 3D
# Vamos definir uma altura para a extrusão
height = 10  # Altura da extrusão (para criar um volume 3D)

# Definindo as coordenadas dos vértices 3D do retângulo extrudido
vertices = np.array(
    [
        [-60, -60, 0],
        [200, -60, 0],
        [200, 60, 0],
        [-60, 60, 0],
        [-60, -60, height],
        [200, -60, height],
        [200, 60, height],
        [-60, 60, height],
    ]
)

# Passo 3: Criar as faces (triângulos) que compõem a superfície
faces = np.array(
    [
        [0, 1, 2],
        [0, 2, 3],  # Base
        [4, 5, 6],
        [4, 6, 7],  # Topo
        [0, 1, 5],
        [0, 5, 4],  # Lado 1
        [1, 2, 6],
        [1, 6, 5],  # Lado 2
        [2, 3, 7],
        [2, 7, 6],  # Lado 3
        [3, 0, 4],
        [3, 4, 7],  # Lado 4
    ]
)

# Passo 4: Criar o objeto STL com os vértices e faces
stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

for i, face in enumerate(faces):
    for j in range(3):
        stl_mesh.vectors[i][j] = vertices[face[j]]

# Passo 5: Salvar como arquivo STL
stl_mesh.save("retangulo_3d.stl")

print("Arquivo STL gerado com sucesso: retangulo_3d.stl")
