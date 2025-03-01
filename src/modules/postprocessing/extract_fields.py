import os
import pyvista as pv
import numpy as np


def extract_fields(vtk_folder):
    """
    Extrai os campos de velocidade e pressão do arquivo VTK.

    Args:
        vtk_folder (str): Caminho para a pasta VTK contendo `internal.vtu`.

    Returns:
        tuple: Arrays numpy de pontos, Ux, Uy e pressão.
    """
    vtk_file = os.path.join(vtk_folder, "internal.vtu")
    if not os.path.exists(vtk_file):
        raise FileNotFoundError(f"Arquivo VTK não encontrado: {vtk_file}")

    dataset = pv.read(vtk_file)
    points_all = dataset.points[:, :2]  # Apenas coordenadas X, Y

    if "U" not in dataset.array_names or "p" not in dataset.array_names:
        raise ValueError(
            f"Campos 'U' ou 'p' não encontrados no arquivo VTK: {vtk_file}"
        )

    velocity = dataset["U"]
    pressure = dataset["p"]

    # ⚠ Certificar-se de que o número de pontos e valores é o mesmo
    min_len = min(len(points_all), len(velocity), len(pressure))
    points = points_all[:min_len]
    Ux, Uy = velocity[:min_len, 0], velocity[:min_len, 1]
    p = pressure[:min_len]

    return points, Ux, Uy, p
