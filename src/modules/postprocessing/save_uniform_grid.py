import os
import numpy as np
from scipy.interpolate import griddata
import pickle


def save_uniform_grid(
    input_dir="processed_data", output_dir="processed_data/uniform_grid"
):
    """
    Interpola os dados extraídos para uma malha estruturada uniforme e os salva.

    Args:
        input_dir (str): Diretório onde os arquivos extraídos (brutos) estão armazenados.
        output_dir (str): Diretório onde os arquivos interpolados serão salvos.
    """
    print(f"🔄 Convertendo dados brutos para malha uniforme...")

    # 🔹 Criar a pasta onde os arquivos da malha uniforme serão salvos
    os.makedirs(output_dir, exist_ok=True)

    # 🔹 Verificar se os arquivos de entrada existem
    files_needed = ["points.npy", "Ux.npy", "Uy.npy", "p.npy"]
    for f in files_needed:
        if not os.path.exists(os.path.join(input_dir, f)):
            print(f"❌ Arquivo {f} não encontrado. Execute a extração primeiro.")
            return False

    # 🔹 Carregar os dados extraídos
    points = np.load(os.path.join(input_dir, "points.npy"))  # (N, 3) coordenadas XYZ
    Ux = np.load(os.path.join(input_dir, "Ux.npy"))  # (N,) velocidade X
    Uy = np.load(os.path.join(input_dir, "Uy.npy"))  # (N,) velocidade Y
    p = np.load(os.path.join(input_dir, "p.npy"))  # (N,) pressão

    # 🔹 Criar a malha uniforme
    grid_x = np.linspace(
        points[:, 0].min(), points[:, 0].max(), 200
    )  # 200 pontos no eixo X
    grid_y = np.linspace(
        points[:, 1].min(), points[:, 1].max(), 100
    )  # 100 pontos no eixo Y
    grid_X, grid_Y = np.meshgrid(grid_x, grid_y)

    # 🔹 Interpolação para a malha uniforme
    def interpolate_to_uniform(points, values, grid_X, grid_Y, method="cubic"):
        grid_values = griddata(points[:, :2], values, (grid_X, grid_Y), method=method)
        return grid_values

    Ux_uniform = interpolate_to_uniform(points, Ux, grid_X, grid_Y, method="cubic")
    Uy_uniform = interpolate_to_uniform(points, Uy, grid_X, grid_Y, method="cubic")
    p_uniform = interpolate_to_uniform(points, p, grid_X, grid_Y, method="cubic")

    # 🔹 Salvar os dados interpolados na malha uniforme
    np.save(os.path.join(output_dir, "Ux_uniform.npy"), Ux_uniform)
    np.save(os.path.join(output_dir, "Uy_uniform.npy"), Uy_uniform)
    np.save(os.path.join(output_dir, "p_uniform.npy"), p_uniform)

    # 🔹 Salvar também no formato `.pkl` para compatibilidade
    uniform_data = {
        "grid_X": grid_X,
        "grid_Y": grid_Y,
        "Ux": Ux_uniform,
        "Uy": Uy_uniform,
        "p": p_uniform,
    }
    with open(os.path.join(output_dir, "uniform_grid.pkl"), "wb") as f:
        pickle.dump(uniform_data, f)

    print(f"✅ Dados salvos na malha uniforme em {output_dir}")
    return True
