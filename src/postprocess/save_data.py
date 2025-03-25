import os
import numpy as np
import h5py
from config import POSTPROCESS_PATH, CLOUD_FILE_NAME, HDF5_FILE_NAME
from utils import get_latest_time  # Importando função auxiliar

def save_hdf5():
    """Carrega os dados do arquivo .xy e salva apenas x, y, p, Ux, Uy em HDF5, com cabeçalhos."""
    
    latest_path = get_latest_time()
    if latest_path is None:
        print("❌ ERRO: Não foi possível encontrar a pasta latestTime.")
        exit()

    file_path = os.path.join(latest_path, CLOUD_FILE_NAME)  # Caminho atualizado corretamente
    hdf5_path = os.path.join(POSTPROCESS_PATH, HDF5_FILE_NAME)  # Caminho completo do arquivo de saída
    
    if not os.path.exists(file_path):
        print(f"❌ ERRO: Arquivo '{file_path}' não encontrado!")
        return

    print(f"📂 [DEBUG] Processando arquivo: {file_path}")

    # Carregar os dados
    data = np.loadtxt(file_path)

    if data.ndim == 1:
        data = data.reshape(1, -1)  # Garantir formato 2D

    # Selecionar apenas as colunas desejadas: x, y, p, Ux, Uy
    filtered_data = data[:, [0, 1, 3, 4, 5]]

    # Nome das colunas armazenadas
    column_names = ["x", "y", "p", "Ux", "Uy"]

    # Criar e salvar o arquivo HDF5
    with h5py.File(hdf5_path, "w") as f:
        f.create_dataset("data", data=filtered_data)
        f.attrs["column_names"] = ",".join(column_names)  # Armazena os cabeçalhos

    print(f"✅ [DEBUG] Arquivo salvo com sucesso: {hdf5_path}")

if __name__ == "__main__":
    save_hdf5()