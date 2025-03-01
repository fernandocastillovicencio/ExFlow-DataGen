import os
import pickle
import numpy as np
import matplotlib.pyplot as plt


def verify_data(output_dir="processed_data", cases_dir="cases/"):
    """
    Verifica a integridade dos arquivos finais dataX.pkl e dataY.pkl.

    Args:
        output_dir (str): Diretório onde os arquivos finais estão armazenados.
        cases_dir (str): Diretório contendo os casos processados.
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

    # Contar o número de pastas de casos processados
    case_dirs = [d for d in os.listdir(cases_dir) if d.startswith("case")]
    num_cases = len(case_dirs)

    # Verificar dimensões
    print(f"✅ Dimensão de dataX: {dataX.shape} (esperado: ({num_cases},3,172,79))")
    print(f"✅ Dimensão de dataY: {dataY.shape} (esperado: ({num_cases},3,172,79))")

    if (
        dataX.shape[1:] != (3, 172, 79)
        or dataY.shape[1:] != (3, 172, 79)
        or dataX.shape[0] != num_cases
    ):
        print("⚠️ Dimensão incorreta detectada! Algo pode estar errado.")
    else:
        print("✅ Dimensões verificadas com sucesso!")

    # Verificação de valores extremos e NaNs
    print(
        f"🔍 Valores de dataX: min={np.nanmin(dataX)}, max={np.nanmax(dataX)}, contém NaN? {np.isnan(dataX).any()}"
    )
    print(
        f"🔍 Valores de dataY: min={np.nanmin(dataY)}, max={np.nanmax(dataY)}, contém NaN? {np.isnan(dataY).any()}"
    )

    if np.isnan(dataX).any() or np.isnan(dataY).any():
        print("⚠️ Os arquivos contêm NaNs! Algo pode estar errado.")
    else:
        print("✅ Nenhum NaN encontrado nos arquivos.")

    print("🔎 Verificação concluída!")


def inspect_sample(output_dir="processed_data", sample_index=0):
    """
    Exibe os valores de uma amostra específica dentro dos arquivos.

    Args:
        output_dir (str): Diretório onde os arquivos finais estão armazenados.
        sample_index (int): Índice da amostra a ser inspecionada.
    """
    dataX_path = os.path.join(output_dir, "dataX.pkl")
    dataY_path = os.path.join(output_dir, "dataY.pkl")

    with open(dataX_path, "rb") as f:
        dataX = pickle.load(f)
    with open(dataY_path, "rb") as f:
        dataY = pickle.load(f)

    if sample_index >= dataX.shape[0]:
        print(
            f"❌ Índice {sample_index} fora do intervalo! Existem apenas {dataX.shape[0]} amostras."
        )
        return

    print(f"🔹 Exibindo amostra {sample_index} de dataX:")
    print(dataX[sample_index])

    print(f"🔹 Exibindo amostra {sample_index} de dataY:")
    print(dataY[sample_index])


def plot_sample(output_dir="processed_data", sample_index=0):
    """
    Plota os campos da amostra específica.

    Args:
        output_dir (str): Diretório onde os arquivos finais estão armazenados.
        sample_index (int): Índice da amostra a ser plotada.
    """
    dataX_path = os.path.join(output_dir, "dataX.pkl")
    dataY_path = os.path.join(output_dir, "dataY.pkl")

    with open(dataX_path, "rb") as f:
        dataX = pickle.load(f)
    with open(dataY_path, "rb") as f:
        dataY = pickle.load(f)

    if sample_index >= dataX.shape[0]:
        print(
            f"❌ Índice {sample_index} fora do intervalo! Existem apenas {dataX.shape[0]} amostras."
        )
        return

    # Extrair os dados
    sdf1 = dataX[sample_index, 0]
    flow_region = dataX[sample_index, 1]
    sdf2 = dataX[sample_index, 2]
    Ux = dataY[sample_index, 0]
    Uy = dataY[sample_index, 1]
    p = dataY[sample_index, 2]

    fig, axs = plt.subplots(2, 3, figsize=(15, 10))

    axs[0, 0].imshow(sdf1, cmap="coolwarm")
    axs[0, 0].set_title("SDF1 (Obstacle Distance)")

    axs[0, 1].imshow(flow_region, cmap="viridis")
    axs[0, 1].set_title("Flow Region")

    axs[0, 2].imshow(sdf2, cmap="coolwarm")
    axs[0, 2].set_title("SDF2 (Wall Distance)")

    axs[1, 0].imshow(Ux, cmap="plasma")
    axs[1, 0].set_title("Velocity Ux")

    axs[1, 1].imshow(Uy, cmap="plasma")
    axs[1, 1].set_title("Velocity Uy")

    axs[1, 2].imshow(p, cmap="magma")
    axs[1, 2].set_title("Pressure")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    verify_data()
    inspect_sample(sample_index=0)
    plot_sample(sample_index=0)
