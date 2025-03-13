from scipy.spatial import cKDTree
import numpy as np


def interpolate_idw(points, values, grid_x, grid_y, power=2):
    """
    Interpola os valores CFD usando Inverse Distance Weighting (IDW).

    - Mantém propriedades físicas do fluxo
    - Melhor preservação de gradientes do que RBF
    - Muito mais rápido para grandes conjuntos de dados

    Args:
        points (array): Coordenadas (X, Y) dos pontos CFD originais.
        values (array): Valores CFD (Ux, Uy ou p).
        grid_x (array): Posições X da malha uniforme (179 pontos).
        grid_y (array): Posições Y da malha uniforme (72 pontos).
        power (int): Peso da distância (default = 2).

    Returns:
        array: Dados interpolados na malha (179x72).
    """
    tree = cKDTree(points)
    grid = np.array(np.meshgrid(grid_x, grid_y)).T.reshape(-1, 2)

    # Encontrar os 4 vizinhos mais próximos
    dists, idxs = tree.query(grid, k=4)

    # Calcular pesos inversos das distâncias
    weights = 1.0 / (dists**power)
    weights /= np.sum(weights, axis=1, keepdims=True)

    # Aplicar interpolação ponderada
    interpolated_values = np.sum(weights * values[idxs], axis=1)

    return interpolated_values.reshape(len(grid_x), len(grid_y)).T
