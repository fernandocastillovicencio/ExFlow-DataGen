# modules/postprocessing/sdf2_generation.py
# Gera a Signed Distance Function (SDF2) considerando as paredes superior e inferior.

import os
import numpy as np
import matplotlib.pyplot as plt
from modules.postprocessing.postprocess_utils import load_vtu_data, create_fixed_grid

def generate_sdf2(vtu_file, grid_width=172, grid_height=79):
    """
    Gera a matriz SDF2, a distância vertical até as paredes superior e inferior.
    """
    coordinates, _, _, _ = load_vtu_data(vtu_file)
    grid_x, grid_y = create_fixed_grid(coordinates, grid_width, grid_height)

    # Obter Y mínimo e máximo (paredes superior e inferior)
    top_wall = np.max(grid_y)
    bottom_wall = np.min(grid_y)

    sdf2 = np.zeros((grid_height, grid_width), dtype=float)
    for i in range(grid_height):
        for j in range(grid_width):
            dist_top = abs(grid_y[i, j] - top_wall)
            dist_bottom = abs(grid_y[i, j] - bottom_wall)
            sdf2[i, j] = min(dist_top, dist_bottom)

    return sdf2

def save_sdf2_image(sdf2, figures_dir):
    """
    Salva a imagem da SDF2 em data/figures/.
    """
    os.makedirs(figures_dir, exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.imshow(sdf2, cmap='jet', origin='lower')
    plt.colorbar(label='Signed Distance Function (SDF2)')
    plt.title('SDF2 (Paredes Sup/Inf)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plot_filename = os.path.join(figures_dir, 'sdf2_visualization.png')
    plt.savefig(plot_filename, dpi=300)
    plt.close()
    print(f"✅ Imagem SDF2 salva em: {plot_filename}")

