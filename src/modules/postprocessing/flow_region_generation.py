# modules/postprocessing/flow_region_generation.py
# Gera a matriz flow_region (0 = obstáculo, 1 = fluido, 2 = bordas superior e inferior, 3 = esquerda, 4 = direita).

import os
import numpy as np
import matplotlib.pyplot as plt
from modules.postprocessing.obstacle_processing import get_obstacle_polygon
from modules.postprocessing.postprocess_utils import load_vtu_data, create_fixed_grid, apply_obstacle_mask

def generate_flow_region(vtu_file, obstacle_file, grid_width=172, grid_height=79):
    """
    Gera a matriz flow_region onde:
      0 = obstáculo,
      1 = fluido,
      2 = bordas superior e inferior,
      3 = borda esquerda,
      4 = borda direita.
    """
    coordinates, _, _, _ = load_vtu_data(vtu_file)
    grid_x, grid_y = create_fixed_grid(coordinates, grid_width, grid_height)

    # 1 = fluido
    flow_region = np.ones((grid_height, grid_width), dtype=int)

    # Obter polígono do obstáculo
    obstacle_polygon = get_obstacle_polygon(obstacle_file)

    # Zerar valores dentro do obstáculo
    flow_region, _, _ = apply_obstacle_mask(flow_region, flow_region, flow_region, grid_x, grid_y, obstacle_polygon)

    # Atribuir 0 ao obstáculo
    # (a função apply_obstacle_mask já definiu 0 dentro, pois substituiu o "flow_region" que era 1 para 0)
    # Caso a lógica seja diferente, ajustar aqui.

    # Definir bordas:
    flow_region[:, 0] = 3   # Esquerda
    flow_region[:, -1] = 4  # Direita
    flow_region[0, :] = 2   # Superior
    flow_region[-1, :] = 2  # Inferior

    return flow_region

def save_flow_region_image(flow_region, figures_dir):
    """
    Salva imagem da matriz flow_region em data/figures/.
    """
    os.makedirs(figures_dir, exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.imshow(flow_region, cmap='jet', origin='lower', alpha=0.8)
    plt.colorbar(ticks=[0, 1, 2, 3, 4], label='Flow Region')
    plt.title('Flow Region')
    plt.xlabel('X')
    plt.ylabel('Y')
    plot_filename = os.path.join(figures_dir, 'flow_region_with_obstacle.png')
    plt.savefig(plot_filename, dpi=300)
    plt.close()
    print(f"✅ Imagem Flow Region salva em: {plot_filename}")
