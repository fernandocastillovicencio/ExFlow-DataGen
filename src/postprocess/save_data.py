import os
import numpy as np
import h5py
from postprocess.config import HDF5_FILE_NAME

def get_latest_time(case_dir):
    """Identifica o maior número de tempo dentro da pasta postProcessing/cloud/ de um caso específico."""
    cloud_path = os.path.join(case_dir, "postProcessing", "cloud")

    if not os.path.exists(cloud_path):
        print(f"❌ ERRO: Diretório {cloud_path} não encontrado!")
        return None

    time_dirs = [d for d in os.listdir(cloud_path) if d.isdigit()]
    if not time_dirs:
        print(f"❌ ERRO: Nenhuma pasta de tempo encontrada em {cloud_path}")
        return None

    latest_time = max(map(int, time_dirs))  # Encontrar o maior número de tempo
    latest_path = os.path.join(cloud_path, str(latest_time))

    return latest_path

def save_hdf5(case_dir):
    """Carrega os dados do arquivo .xy e salva apenas x, y, p, Ux, Uy em HDF5 dentro do caso especificado."""
    
    latest_path = get_latest_time(case_dir)
    if latest_path is None:
        return

    file_path = os.path.join(latest_path, "ref_point_p_U.xy")  # Nome fixo do arquivo de entrada
    hdf5_path = os.path.join(case_dir, HDF5_FILE_NAME)  # Caminho do arquivo de saída

    if not os.path.exists(file_path):
        print(f"❌ ERRO: Arquivo '{file_path}' não encontrado em {latest_path}!")
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

    # Criar e salvar o arquivo HDF5 dentro da pasta do caso
    with h5py.File(hdf5_path, "w") as f:
        f.create_dataset("data", data=filtered_data)
        f.attrs["column_names"] = ",".join(column_names)  # Armazena os cabeçalhos

    print(f"✅ [DEBUG] Arquivo salvo com sucesso: {hdf5_path}")

def main(case_dir):
    """Executa a conversão dos dados de um caso específico para o formato HDF5."""
    save_hdf5(case_dir)
