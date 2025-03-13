import os
import numpy as np
import pickle
import random
import subprocess
import shutil
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator, griddata

# 📂 Diretório base onde os cases estão
CASES_DIR = "cases"

# 📌 Resolver links simbólicos, caso existam
if os.path.islink(CASES_DIR):
    CASES_DIR = os.path.realpath(CASES_DIR)  # Obtém o caminho real do link

PROCESSED_DIR = "processed_data"

# 🔄 Escolher um caso aleatório dentro da pasta "cases/"
cases = [c for c in os.listdir(CASES_DIR) if os.path.isdir(os.path.join(CASES_DIR, c))]
selected_case = random.choice(cases)
case_path = os.path.join(CASES_DIR, selected_case)
processed_path = os.path.join(case_path, "processed")

print(f"🔄 Testando pós-processamento no caso aleatório: {selected_case}")
print(f"📂 Caminho real da pasta cases: {CASES_DIR}")

# 📌 1️⃣ Verificar se os arquivos `dataX.npy` e `dataY.npy` já existem
dataX_path = os.path.join(processed_path, "dataX.npy")
dataY_path = os.path.join(processed_path, "dataY.npy")

if not os.path.exists(dataX_path) or not os.path.exists(dataY_path):
    print(f"❌ Arquivos processados não encontrados! Executando extração automática...")

    # Executar extração automática com caminho real
    extraction_script = "src/modules/postprocessing/extract_vtk_data.py"
    try:
        result = subprocess.run(
            ["python", extraction_script, case_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✅ Extração executada! Saída:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar `extract_vtk_data.py`: {e}")
        print(f"🔍 Saída de erro:\n{e.stderr}")
        exit()

# 📌 2️⃣ Verificar se os arquivos foram realmente gerados após a extração
if os.path.exists(dataX_path) and os.path.exists(dataY_path):
    print(f"✅ Arquivos `dataX.npy` e `dataY.npy` encontrados!")
else:
    print(
        f"❌ Erro: Os arquivos `dataX.npy` e `dataY.npy` ainda não foram gerados após a extração."
    )
    exit()

# 📌 3️⃣ Carregar os arquivos `.npy`
try:
    dataX = np.load(dataX_path)  # Pode estar no formato (3, 172, 79)
    dataY = np.load(dataY_path)  # Pode estar no formato (3, 172, 79)
    print(
        f"✅ `dataX.npy` e `dataY.npy` carregados com sucesso! Shape dataX: {dataX.shape}, dataY: {dataY.shape}"
    )
except FileNotFoundError as e:
    print(f"❌ Erro ao carregar arquivos `.npy`: {e}")
    exit()

# 📌 4️⃣ Ajustar a Dimensão N=1 se Necessário
if dataX.shape == (3, 172, 79):
    dataX = np.expand_dims(
        dataX, axis=0
    )  # Adicionar dimensão N=1 para manter compatibilidade
if dataY.shape == (3, 172, 79):
    dataY = np.expand_dims(
        dataY, axis=0
    )  # Adicionar dimensão N=1 para manter compatibilidade

# 📌 5️⃣ Salvar os arquivos `.npy` processados na pasta `processed_data/`
if not os.path.exists(PROCESSED_DIR):
    os.makedirs(PROCESSED_DIR)

np.save(os.path.join(PROCESSED_DIR, "dataX_processed.npy"), dataX)
np.save(os.path.join(PROCESSED_DIR, "dataY_processed.npy"), dataY)

print("✅ Arquivos `.npy` processados foram salvos com sucesso!")


# 📌 6️⃣ Aplicar Interpolação RBF para Melhor Precisão
def interpolate_field(grid_x, grid_y, values):
    """
    Interpola os valores CFD para uma malha estruturada usando RBFInterpolator (Thin Plate Spline).
    Se falhar, usa interpolação cúbica como fallback.
    """
    X_DIM, Y_DIM = 172, 79
    grid_X, grid_Y = np.meshgrid(grid_x, grid_y, indexing="ij")

    points = np.column_stack((grid_X.ravel(), grid_Y.ravel()))

    try:
        interpolator = RBFInterpolator(
            points, values.ravel(), kernel="thin_plate_spline"
        )
        return interpolator(points).reshape(grid_X.shape)
    except:
        print("⚠ RBF falhou! Usando interpolação cúbica como fallback...")
        return griddata(
            points, values.ravel(), (grid_X, grid_Y), method="cubic"
        ).reshape(grid_X.shape)


# 📌 7️⃣ Criar Grid Refinado para Suavização
grid_x = np.linspace(-1, 1, 172)
grid_y = np.linspace(-1, 1, 79)

# 📌 8️⃣ Interpolar os Campos com Maior Precisão
Ux_interp = interpolate_field(grid_x, grid_y, dataY[0, 0, :, :])
Uy_interp = interpolate_field(grid_x, grid_y, dataY[0, 1, :, :])
p_interp = interpolate_field(grid_x, grid_y, dataY[0, 2, :, :])

sdf1_interp = interpolate_field(grid_x, grid_y, dataX[0, 0, :, :])
flow_region_interp = interpolate_field(grid_x, grid_y, dataX[0, 1, :, :])
sdf2_interp = interpolate_field(grid_x, grid_y, dataX[0, 2, :, :])


# 📌 9️⃣ Salvar as imagens dos campos gerados para inspeção
def plot_and_save(data, title, filename):
    plt.figure(figsize=(8, 6))
    plt.imshow(data, cmap="jet", origin="lower")
    plt.colorbar(label="Magnitude")
    plt.title(title)
    plt.xlabel("X (grid points)")
    plt.ylabel("Y (grid points)")
    plt.grid(False)
    plt.savefig(os.path.join(PROCESSED_DIR, filename))
    plt.close()


plot_and_save(Ux_interp, "Velocidade Ux", "Ux_interpolated.png")
plot_and_save(Uy_interp, "Velocidade Uy", "Uy_interpolated.png")
plot_and_save(p_interp, "Pressão", "p_interpolated.png")
plot_and_save(sdf1_interp, "SDF1 (Obstáculo)", "SDF1_interpolated.png")
plot_and_save(flow_region_interp, "Flow Region", "FlowRegion_interpolated.png")
plot_and_save(sdf2_interp, "SDF2 (Paredes Laterais)", "SDF2_interpolated.png")

print("✅ Todas as imagens foram geradas e salvas em `processed_data/`!")
