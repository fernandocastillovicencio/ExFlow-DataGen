# src/modules/geometry/transform_utils.py
"""
Transformation utilities for shape deformation and rotation.

This module provides functions to apply various transformations to geometric shapes,
including stretching and rotating shapes. The functions are designed to handle both
2D and 3D shapes.

Functions:
- stretch_one_side(vertices, deformation_factor, side): Applies horizontal deformation
  to one half of the shape, either left or right.
- stretch_both_sides(vertices, left_factor, right_factor): Applies different horizontal
  deformations to the left and right halves of the shape.
- rotate_shape(vertices, angle_degrees): Rotates a shape counterclockwise around (0,0)
  by a given angle, handling both 2D and 3D shapes.
- merge_shapes(vertices1, faces1): Merges two semicircles to create a full circle by
  rotating the first semicircle by 180 degrees and combining the vertices and faces.
"""

import numpy as np


def shear_horizontal(vertices, shear_factor):
    """
    Apply horizontal shear transformation to the shape.

    Parameters:
        vertices (np.ndarray): Shape vertices (N,3).
        shear_factor (float): Shear factor to control the magnitude of shearing.

    Returns:
        np.ndarray: Sheared vertices.
    """
    # Apply shear transformation
    sheared_vertices = vertices.copy()

    # Apply shear to each vertex
    sheared_vertices[:, 0] += (
        shear_factor * sheared_vertices[:, 1]
    )  # shear factor applied to x

    return sheared_vertices


def rotate_shapes(vertices, angle_degrees):
    """
    Rotate a shape counterclockwise around (0,0) by a given angle.

    This function handles both 2D and 3D vertices. The rotation is done in the XY plane
    for 3D shapes, effectively rotating the shape around the Z-axis.

    Parameters:
        vertices (np.ndarray): Shape vertices (N, 2 or 3), with optional z=0 for 2D shapes.
        angle_degrees (float): Rotation angle in degrees.

    Returns:
        np.ndarray: Rotated vertices (N, 2 or 3).
    """
    # Convert angle from degrees to radians
    angle_radians = np.radians(angle_degrees)

    # Check if the shape is 2D or 3D (check if z exists in the vertices)
    if vertices.shape[1] == 2:  # 2D
        # Rotation matrix for 2D rotation
        rotation_matrix = np.array(
            [
                [np.cos(angle_radians), -np.sin(angle_radians)],
                [np.sin(angle_radians), np.cos(angle_radians)],
            ]
        )
        # Apply rotation to x and y, z remains unchanged (implicitly)
        rotated_vertices = vertices @ rotation_matrix.T
        return rotated_vertices

    elif vertices.shape[1] == 3:  # 3D
        # Rotation matrix for 3D rotation in the XY plane
        rotation_matrix = np.array(
            [
                [np.cos(angle_radians), -np.sin(angle_radians), 0],
                [np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1],
            ]
        )
        # Apply rotation to x, y and z (rotation in the XY plane)
        rotated_vertices = vertices @ rotation_matrix.T
        return rotated_vertices

    else:
        raise ValueError("Vertices must have 2 or 3 columns (2D or 3D shapes).")


def merge_shapes(vertices1, faces1):
    """
    Merge two semicircles to create a full circle.

    This function takes the vertices and faces of one semicircle, creates a second
    semicircle by rotating the first one by 180 degrees, and then merges both to
    create a full circle.

    Parameters:
        vertices1 (np.ndarray): Vertices of the first semicircle (N,3).
        faces1 (list): Faces of the first semicircle.

    Returns:
        tuple: (vertices, faces) - Full merged shape.
    """
    # Create a rotation matrix to rotate the first semicircle by 180 degrees.
    # This is equivalent to flipping the x and y axes.
    rotation_matrix = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])

    # Apply the rotation matrix to the vertices of the first semicircle to create
    # the second semicircle.
    vertices2 = vertices1 @ rotation_matrix.T

    # Offset the face indices of the second semicircle by the length of the first
    # semicircle. This is because the faces of the second semicircle are computed
    # relative to the vertices of the first semicircle.
    faces2 = (np.array(faces1) + len(vertices1)).tolist()

    # Merge the vertices and faces of both semicircles to create the full circle.
    vertices = np.vstack((vertices1, vertices2))
    faces = faces1 + faces2

    return vertices, faces


# ---------------------------------------------------------------------------- #

import numpy as np
from shapely.geometry import Polygon


def rotate_shape(geometry, angle_deg, center=(0, 0)):
    """
    Gira a geometria (Polygon) pelo ângulo especificado.

    Parameters:
        geometry (Polygon): A geometria a ser rotacionada.
        angle_deg (float): O ângulo de rotação em graus.
        center (tuple): O ponto de rotação (default é (0, 0)).

    Returns:
        Polygon: A geometria rotacionada.
    """
    # Converte o ângulo de graus para radianos
    angle_rad = np.radians(angle_deg)

    # Matriz de rotação 2D
    rotation_matrix = np.array(
        [
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad), np.cos(angle_rad)],
        ]
    )

    # Função para rotacionar os vértices de um polígono
    def rotate_vertices(vertices):
        # Subtrai o centro da geometria para que a rotação seja em torno do centro
        rotated = []
        for x, y in vertices:
            x_new, y_new = np.dot(
                rotation_matrix, np.array([x - center[0], y - center[1]])
            )
            rotated.append(
                (x_new + center[0], y_new + center[1])
            )  # Revertendo a translação
        return rotated

    # Rotacionando a geometria
    if isinstance(geometry, Polygon):
        # Para Polygon, apenas rotacionamos os pontos do exterior
        exterior_coords = rotate_vertices(list(geometry.exterior.coords))
        return Polygon(exterior_coords)
    else:
        raise ValueError("A geometria deve ser um Polygon do Shapely.")


# ---------------------------------------------------------------------------- #

import numpy as np
from shapely.geometry import Polygon


def stretch_one_side(geometry, side, factor):
    """
    Alongar apenas um lado da geometria (esquerdo ou direito).

    Parameters:
        geometry (Polygon): A geometria a ser alongada.
        factor (float): O fator de alongamento.
        side (str): 'left' para alongar o lado esquerdo (x <= 0), 'right' para o lado direito (x >= 0).

    Returns:
        Polygon: A geometria com o lado especificado alongado.
    """
    if side not in ["left", "right"]:
        raise ValueError("O argumento 'side' deve ser 'left' ou 'right'.")

    # Obter os vértices da geometria
    vertices = np.array([list(coord) + [0] for coord in geometry.exterior.coords])

    # Alongar a metade especificada
    if side == "left":
        # Alongar os vértices com x <= 0
        vertices[vertices[:, 0] <= 0, 0] *= factor
    else:
        # Alongar os vértices com x >= 0
        vertices[vertices[:, 0] >= 0, 0] *= factor

    # Retornar a geometria com os vértices alterados
    return Polygon(vertices[:, :2])


def stretch_both_sides(geometry, factor):
    """
    Alongar ambos os lados da geometria (x <= 0 e x >= 0) com o mesmo fator.

    Parameters:
        geometry (Polygon): A geometria a ser alongada.
        factor (float): O fator de alongamento para ambos os lados.

    Returns:
        Polygon: A geometria com ambos os lados alongados.
    """
    # Obter os vértices da geometria
    vertices = np.array([list(coord) + [0] for coord in geometry.exterior.coords])

    # Alongar ambos os lados (esquerdo e direito)
    vertices[vertices[:, 0] <= 0, 0] *= factor
    vertices[vertices[:, 0] >= 0, 0] *= factor

    # Retornar a geometria com os vértices alterados
    return Polygon(vertices[:, :2])
