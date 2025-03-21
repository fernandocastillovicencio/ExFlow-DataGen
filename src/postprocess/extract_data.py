import numpy as np
import os
from .config import POSTPROCESS_PATH, X_MIN, X_MAX, NX, Y_MIN, Y_MAX, NY

def read_xy_file(file_path):
    """Lê um arquivo .xy e retorna y e Ux."""
    data = np.loadtxt(file_path)
    y, Ux = data[:, 0], data[:, 2]  # Terceira coluna é Ux
    return y, Ux

def process_Ux_field():
    """Processa os arquivos .xy e cria a matriz Ux."""
    x_values = np.linspace(X_MIN, X_MAX, NX + 1)
    x_centers = np.round((x_values[:-1] + x_values[1:]) / 2, 3)
    files = sorted([f for f in os.listdir(POSTPROCESS_PATH) if f.endswith('.xy')])

    Ux_field = np.zeros((NY, NX))

    for i, file_name in enumerate(files):
        file_path = os.path.join(POSTPROCESS_PATH, file_name)
        y, Ux = read_xy_file(file_path)

        for j in range(len(y)):
            y_index = int(np.round((y[j] - Y_MIN) / (Y_MAX - Y_MIN) * (NY - 1)))
            y_index = np.clip(y_index, 0, NY - 1)
            x_index = i
            x_index = np.clip(x_index, 0, NX - 1)
            Ux_field[y_index, x_index] = Ux[j]

    return Ux_field
