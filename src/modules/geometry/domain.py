import numpy as np
from shapely.geometry import Polygon
from stl import mesh


def create_2d_rectangle(width=4, height=4):
    """
    Cria um retângulo simplesaa.
    """
    return Polygon(
        [
            (-width / 2, -height / 2),
            (width / 2, -height / 2),
            (width / 2, height / 2),
            (-width / 2, height / 2),
        ]
    )


def create_2d_circle(center=(0, 0), radius=1.0, num_points=100):
    """
    Cria um círculo simples.
    """
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = radius * np.cos(theta) + center[0]
    y = radius * np.sin(theta) + center[1]
    points = list(zip(x, y))
    points.append(points[0])  # Fecha o círculo
    return Polygon(points)


def extrude_2d_to_3d(geometry, height=1.0):
    """
    Extruda a geometria 2D para 3D, criando uma forma prismática com a altura fornecida.
    """
    vertices = []
    faces = []

    # Criar vértices para a geometria extrudada (duas camadas, uma na base e outra no topo)
    for i, (x, y) in enumerate(geometry.exterior.coords):
        vertices.append([x, y, 0])  # Base
        vertices.append([x, y, height])  # Topo

    # Criar faces (triângulos ou quadrados conectando a base e o topo)
    num_points = (
        len(geometry.exterior.coords) - 1
    )  # Exclui o ponto final que é igual ao inicial
    for i in range(num_points):
        next_i = (i + 1) % num_points
        # Faces laterais
        faces.append([i * 2, next_i * 2, next_i * 2 + 1])
        faces.append([i * 2, next_i * 2 + 1, i * 2 + 1])
        # Faces do topo e da base
        if i < num_points - 1:
            faces.append([i * 2, next_i * 2, next_i * 2 + 1])
            faces.append([i * 2, next_i * 2 + 1, i * 2 + 1])

    return vertices, faces


# -------------------------------------------------------- #
def exporting_stl(vertices, faces, filename="output.stl"):
    """
    Converte os vértices e faces em uma malha STL e salva o arquivo.
    """
    model = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        for j in range(3):
            model.vectors[i][j] = vertices[f[j]]

    model.save(filename)
    print(f"STL gerado com sucesso: {filename}")


from stl import mesh
import numpy as np


def exporting_stl_ascii(vertices, faces, filename="output.stl"):
    """
    Converte os vértices e faces em uma malha STL e salva o arquivo em formato ASCII.
    """
    # Criar a malha a partir dos vértices e faces
    model = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))

    for i, f in enumerate(faces):
        for j in range(3):
            model.vectors[i][j] = vertices[f[j]]

    # Agora, escrever manualmente o arquivo em formato ASCII
    with open(filename, "w") as ascii_file:
        ascii_file.write("solid shape\n")
        for i, f in enumerate(faces):
            v0, v1, v2 = [model.vectors[i][j] for j in range(3)]
            ascii_file.write("  facet normal 0 0 0\n")
            ascii_file.write("    outer loop\n")
            ascii_file.write(f"      vertex {v0[0]} {v0[1]} {v0[2]}\n")
            ascii_file.write(f"      vertex {v1[0]} {v1[1]} {v1[2]}\n")
            ascii_file.write(f"      vertex {v2[0]} {v2[1]} {v2[2]}\n")
            ascii_file.write("    endloop\n")
            ascii_file.write("  endfacet\n")
        ascii_file.write("endsolid shape\n")

    print(f"STL gerado com sucesso (ASCII): {filename}")


# -------------------------------------------------------- #
def main():
    # Criar formas 2D
    rectangle = create_2d_rectangle(width=4, height=4)
    circle = create_2d_circle(center=(0, 0), radius=1.0)

    # Extrudar as formas 2D para 3D
    rectangle_vertices, rectangle_faces = extrude_2d_to_3d(rectangle, height=2.0)
    circle_vertices, circle_faces = extrude_2d_to_3d(circle, height=2.0)

    # Salvar ambos os sólidos como arquivos STL
    exporting_stl(rectangle_vertices, rectangle_faces, "rectangle_3d.stl")
    exporting_stl(circle_vertices, circle_faces, "circle_3d.stl")


# Executar o script
if __name__ == "__main__":
    main()
