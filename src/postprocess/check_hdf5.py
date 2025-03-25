import os
import h5py
import numpy as np
from config import POSTPROCESS_PATH, HDF5_FILE_NAME  # Importando caminho do arquivo HDF5

def check_hdf5():
    """Carrega o arquivo HDF5 gerado e exibe as informações armazenadas."""
    
    # Caminho do arquivo HDF5
    hdf5_path = os.path.join(POSTPROCESS_PATH, HDF5_FILE_NAME)

    if not os.path.exists(hdf5_path):
        print(f"❌ ERRO: Arquivo '{hdf5_path}' não encontrado!")
        return

    print(f"📂 [DEBUG] Abrindo arquivo: {hdf5_path}")

    # Abrir o arquivo HDF5 para leitura
    with h5py.File(hdf5_path, "r") as f:
        # Verificar os atributos armazenados (nomes das colunas)
        column_names = f.attrs["column_names"].split(",")  # Recuperar os cabeçalhos
        data = np.array(f["data"])  # Carregar os dados armazenados

    # Exibir informações
    print("\n📌 **Cabeçalhos Armazenados:**", column_names)
    print("\n🔍 **Amostra dos Dados Salvos:**")
    print(data[:5])  # Exibir as primeiras 5 linhas

if __name__ == "__main__":
    check_hdf5()
