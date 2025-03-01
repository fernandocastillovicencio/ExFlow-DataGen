from scipy.interpolate import griddata
import numpy as np


def interpolate_fields(points, Ux, Uy, p, grid_x, grid_y):
    """
    Interpola os campos de velocidade e pressão para a grade `(172, 79)`.

    Args:
        points (array): Coordenadas X e Y.
        Ux (array): Velocidade em X.
        Uy (array): Velocidade em Y.
        p (array): Pressão.
        grid_x (array): Malha X.
        grid_y (array): Malha Y.

    Returns:
        tuple: Arrays interpolados para Ux, Uy e p.
    """
    X, Y = np.meshgrid(grid_x, grid_y)
    Ux_grid = griddata(points, Ux, (X, Y), method="nearest")
    Uy_grid = griddata(points, Uy, (X, Y), method="nearest")
    p_grid = griddata(points, p, (X, Y), method="nearest")

    return Ux_grid.T, Uy_grid.T, p_grid.T  # Transpor para (172, 79)
