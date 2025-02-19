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


from shapely.geometry import Polygon


def translate_shape(shape, dx=0.0, dy=0.0):
    """
    Translada uma geometria 2D no plano XY, garantindo que a geometria seja um Polygon válido.

    Parameters:
        shape (Polygon): A geometria (Polygon) a ser transladada.
        dx (float): Deslocamento ao longo do eixo X.
        dy (float): Deslocamento ao longo do eixo Y.

    Returns:
        Polygon: A geometria transladada (Polygon).
    """
    # if not isinstance(shape, Polygon):
    #     raise ValueError("A geometria deve ser um Polygon do Shapely.")

    # Obtém as coordenadas do exterior do polígono
    coords = list(shape.exterior.coords)

    # Aplica a translação nos pontos
    translated_coords = [(x + dx, y + dy) for x, y in coords]

    # Cria um novo Polygon com os pontos transladados
    return Polygon(translated_coords)


# -------------------------------------------------------- #

import numpy as np


def rotate_shape(geometry, angle_degrees):
    """
    Rotaciona uma geometria 2D (Polygon do Shapely ou array de vértices) a partir de um ângulo dado.
    A rotação é feita no plano XY para 2D.

    Parameters:
        geometry (Polygon or np.ndarray): Geometria do Shapely ou array de vértices (N,2).
        angle_degrees (float): O ângulo de rotação em graus.

    Returns:
        Polygon: Geometria rotacionada (caso seja Shapely).
        np.ndarray: Vértices rotacionados (caso seja array NumPy).
    """
    # Se for um objeto Shapely, extrai os vértices e converte para array NumPy
    if isinstance(geometry, Polygon):
        vertices = np.array(geometry.exterior.coords)
    else:
        vertices = np.array(geometry)

    # Garantir que há pelo menos uma dimensão válida para multiplicação
    if vertices.ndim == 1:
        vertices = vertices.reshape(1, -1)

    # Converter o ângulo de graus para radianos
    angle_radians = np.radians(angle_degrees)

    # Matriz de rotação 2D (para a rotação no plano XY)
    rotation_matrix = np.array(
        [
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians), np.cos(angle_radians)],
        ]
    )

    # Aplicando a rotação
    rotated_vertices = vertices[:, :2] @ rotation_matrix.T  # Multiplicação matricial

    # Se a entrada era um Polygon, retorna um Polygon rotacionado
    if isinstance(geometry, Polygon):
        return Polygon(rotated_vertices)

    return rotated_vertices


# -------------------------------------------------------- #
