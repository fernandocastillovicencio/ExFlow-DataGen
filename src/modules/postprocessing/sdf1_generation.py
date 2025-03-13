# modules/postprocessing/sdf1_generation.py
# Gera a Signed Distance Function (SDF1) para o obstáculo.

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from modules.postprocessing.obstacle_processing import get_obstacle_polygon
from modules.postprocessing.postprocess_utils import create_fixed_grid, load_vtu_data, apply_obstacle_mask

def generate_sdf1(vtu_file, obstacle_file, grid_width=172, grid_height=79):
    """
    Gera a matriz SDF1 (Signed Distance Function) baseada no obstáculo.
    
    Args:
        vtu_file (str): Caminho do arquivo VTU (internal.vtu).
        obstacle_file (str): Caminho do arquivo de obstáculo (wall.vtp).
        grid_width (int): Largura da grade.
        grid_height (int): Altura da grade.
    Returns:
        sdf1 (np.ndarray): Matriz do SDF1 com dimensões (grid_height, grid_width).
    """

    # 1) Carregar dados e gerar grade
    coordinates, _, _, _ = load_vtu_data(vtu_file)
    grid_x, grid_y = create_fixed_grid(coordinates, grid_width, grid_height)
    
    # 2) Inicia array de "fluido" para identificar a região de obstáculo
    flow_region = np.ones((grid_height, grid_width), dtype=int)

    # 3) Obter polígono do obstáculo e aplicar máscara
    obstacle_polygon = get_obstacle_polygon(obstacle_file)
    flow_region, _, _ = apply_obstacle_mask(
        flow_region, flow_region, flow_region, grid_x, grid_y, obstacle_polygon
    )

    # 4) Criar lista de pontos do contorno do obstáculo e inicializar SDF
    obstacle_boundary = np.array(obstacle_polygon.exterior.coords)
    tree = cKDTree(obstacle_boundary)
    sdf1 = np.zeros_like(flow_region, dtype=float)

    for i in range(grid_height):
        for j in range(grid_width):
            dist = tree.query([grid_x[i, j], grid_y[i, j]])[0]
            # Se for dentro do obstáculo, SDF é negativo
            if flow_region[i, j] == 0:
                sdf1[i, j] = -dist
            else:
                sdf1[i, j] = dist

    return sdf1

def save_sdf1_image(sdf1, figures_dir):
    """
    Salva a imagem da SDF1 em data/figures/.
    """
    os.makedirs(figures_dir, exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.imshow(sdf1, cmap='jet', origin='lower')
    plt.colorbar(label='Signed Distance Function (SDF1)')
    plt.title('SDF1 (Obstáculo)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plot_filename = os.path.join(figures_dir, 'sdf1_visualization.png')
    plt.savefig(plot_filename, dpi=300)
    plt.close()
    print(f"✅ Imagem SDF1 salva em: {plot_filename}")
