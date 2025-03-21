import numpy as np
import matplotlib.pyplot as plt
from .config import OUTPUT_NPY_PATH, X_MIN, X_MAX, Y_MIN, Y_MAX

def plot_Ux_field():
    """Plota o campo Ux salvo no arquivo .npy."""
    Ux_field = np.load(OUTPUT_NPY_PATH)

    plt.figure(figsize=(8, 6))
    plt.imshow(Ux_field, cmap='jet', origin='lower', extent=[X_MIN, X_MAX, Y_MIN, Y_MAX])
    plt.colorbar(label='Velocidade Ux (m/s)')
    plt.xlabel('Posição X')
    plt.ylabel('Posição Y')
    plt.title('Campo de Velocidade Ux')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_Ux_field()
