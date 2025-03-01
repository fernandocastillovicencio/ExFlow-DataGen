import os
import pickle
import numpy as np


def verify_data(output_dir="processed_data"):
    """
    Verifica a integridade dos arquivos dataX.pkl e dataY.pkl.

    Args:
        output_dir (str): Diretório onde os arquivos finais estão armazenados.
    """
    dataX_path = os.path.join(output_dir, "dataX.pkl")
    dataY_path = os.path.join(output_dir, "dataY.pkl")

    # Verificar se os arquivos existem
    if not os.path.exists(dataX_path) or not os.path.exists(dataY_path):
        print("❌ Arquivos dataX.pkl ou dataY.pkl não encontrados!")
        return

    # Carregar os arquivos
    with open(dataX_path, "rb") as f:
        dataX = pickle.load(f)
    with open(dataY_path, "rb") as f:
        dataY = pickle.load(f)

    # Verificar a dimensão correta (N, 3, 172, 79)
    print(f"✅ Dimensão de dataX: {dataX.shape} (esperado: (N,3,172,79))")
    print(f"✅ Dimensão de dataY: {dataY.shape} (esperado: (N,3,172,79))")

    if dataX.shape[1:] != (3, 172, 79) or dataY.shape[1:] != (3, 172, 79):
        print("⚠️ Dimensão incorreta detectada! Algo pode estar errado.")

    # Verificar valores mínimos e máximos para garantir que os dados não estão vazios
    print(f"🔍 Valores de dataX: min={dataX.min()}, max={dataX.max()}")
    print(f"🔍 Valores de dataY: min={dataY.min()}, max={dataY.max()}")


if __name__ == "__main__":
    verify_data()
