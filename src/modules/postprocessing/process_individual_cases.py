import os
import numpy as np
from modules.postprocessing.extract_fields import extract_fields
from modules.postprocessing.interpolate_fields import interpolate_rbf

# 🔹 Definir a nova malha estruturada
grid_x = np.linspace(-0.060, 0.200, 179)  # 179 pontos no eixo X
grid_y = np.linspace(-0.060, 0.060, 72)  # 72 pontos no eixo Y


def process_case(case_dir):
    """
    Processa um caso individual, extraindo os campos e aplicando interpolação RBF.

    Args:
        case_dir (str): Caminho para o diretório do caso CFD.
    """
    vtk_folder = os.path.join(case_dir, "VTK")

    # Verificar se os arquivos VTK existem
    if not os.path.exists(vtk_folder):
        print(f"❌ Arquivos VTK não encontrados em {case_dir}")
        return

    # Extrair pontos e campos CFD
    points, Ux, Uy, p = extract_fields(vtk_folder)

    # Aplicar interpolação RBF para cada variável
    Ux_interp = interpolate_rbf(points, Ux, grid_x, grid_y)
    Uy_interp = interpolate_rbf(points, Uy, grid_x, grid_y)
    p_interp = interpolate_rbf(points, p, grid_x, grid_y)

    # Salvar os dados interpolados
    processed_dir = os.path.join(case_dir, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    np.save(os.path.join(processed_dir, "Ux_interp.npy"), Ux_interp)
    np.save(os.path.join(processed_dir, "Uy_interp.npy"), Uy_interp)
    np.save(os.path.join(processed_dir, "p_interp.npy"), p_interp)

    print(f"✅ Interpolação concluída e salva em {processed_dir}")
