import os
import numpy as np
import random
import matplotlib.pyplot as plt
from modules.postprocessing.extract_vtk_data import (
    extract_vtk_data,
)  # Importa a função de extração

# 🔹 Diretório onde estão os casos OpenFOAM
CASES_DIR = "cases"

# 🔹 Selecionar um caso aleatório
case_dirs = [d for d in os.listdir(CASES_DIR) if d.startswith("case")]
if not case_dirs:
    print(
        "❌ Nenhum caso encontrado em 'cases/'. Certifique-se de que há simulações finalizadas."
    )
    exit()

CASE_NAME = random.choice(case_dirs)  # Sorteia um caso aleatório
CASE_DIR = os.path.join(CASES_DIR, CASE_NAME)

print(f"🔄 Testando pós-processamento no caso aleatório: {CASE_NAME}")

# 🔹 Executar a extração dos dados do VTK sem interpolação
extract_vtk_data(CASE_DIR)  # Chama a função de extração para o caso sorteado

# 🔹 Diretório onde os dados serão armazenados
DATA_DIR = "processed_data"

# 🔹 Carregar os arquivos `.npy` gerados pela extração
points_file = os.path.join(DATA_DIR, "points.npy")
Ux_file = os.path.join(DATA_DIR, "Ux.npy")
Uy_file = os.path.join(DATA_DIR, "Uy.npy")
p_file = os.path.join(DATA_DIR, "p.npy")

# 🔹 Verificar se os arquivos foram gerados corretamente
for f in [points_file, Ux_file, Uy_file, p_file]:
    if not os.path.exists(f):
        print(f"❌ Arquivo {f} não encontrado. Algo deu errado na extração.")
        exit()

# 🔹 Carregar os dados extraídos
points = np.load(points_file)  # (N, 3) coordenadas XYZ
Ux = np.load(Ux_file)  # (N,) velocidade X
Uy = np.load(Uy_file)  # (N,) velocidade Y
p = np.load(p_file)  # (N,) pressão

# 🔹 Criar uma malha estruturada regular para interpolação (sem alterar dados brutos)
grid_x = np.linspace(points[:, 0].min(), points[:, 0].max(), 200)
grid_y = np.linspace(points[:, 1].min(), points[:, 1].max(), 100)
grid_X, grid_Y = np.meshgrid(grid_x, grid_y)


# 🔹 Função para plotar os campos extraídos sem interpolação
def plot_scatter(X, Y, values, title, filename, cmap="jet"):
    plt.figure(figsize=(8, 6))
    plt.scatter(X, Y, c=values, cmap=cmap, s=5, marker="o")
    plt.colorbar(label="Magnitude")
    plt.title(title)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig(os.path.join(DATA_DIR, filename))
    plt.show()


# 🔹 Gerar os plots dos campos brutos
plot_scatter(
    points[:, 0], points[:, 1], Ux, "Velocidade Ux (sem interpolação)", "Ux_raw.png"
)
plot_scatter(
    points[:, 0], points[:, 1], Uy, "Velocidade Uy (sem interpolação)", "Uy_raw.png"
)
plot_scatter(points[:, 0], points[:, 1], p, "Pressão (sem interpolação)", "p_raw.png")

print("✅ Teste de pós-processamento concluído com sucesso!")
