import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import random


def plot_sample(output_dir="processed_data", sample_index=None):
    """
    Plota os seis campos da amostra específica e salva os gráficos separadamente em `processed_data/visualizations/`.

    Args:
        output_dir (str): Diretório onde os arquivos finais estão armazenados.
        sample_index (int, opcional): Índice da amostra a ser plotada. Se None, seleciona um índice aleatório.
    """
    dataX_path = os.path.join(output_dir, "dataX.pkl")
    dataY_path = os.path.join(output_dir, "dataY.pkl")

    # Criar a pasta `processed_data/visualizations/` caso não exista
    visualization_dir = os.path.join(output_dir, "visualizations")
    os.makedirs(visualization_dir, exist_ok=True)

    with open(dataX_path, "rb") as f:
        dataX = pickle.load(f)
    with open(dataY_path, "rb") as f:
        dataY = pickle.load(f)

    # Se nenhum índice for fornecido, escolher um índice aleatório
    if sample_index is None:
        sample_index = random.randint(0, dataX.shape[0] - 1)
        print(f"🔀 Amostra aleatória selecionada: {sample_index}")

    if sample_index >= dataX.shape[0]:
        print(
            f"❌ Índice {sample_index} fora do intervalo! Existem apenas {dataX.shape[0]} amostras."
        )
        return

    # Extração correta das imagens (pegar a amostra específica no índice certo)
    sdf1 = dataX[sample_index, 0, :, :]
    flow_region = dataX[sample_index, 1, :, :]
    sdf2 = dataX[sample_index, 2, :, :]
    Ux = dataY[sample_index, 0, :, :]
    Uy = dataY[sample_index, 1, :, :]
    p = dataY[sample_index, 2, :, :]

    # Lista de dados para plotar com o cmap correto
    campos = [
        (sdf1, "SDF1 (Obstacle Distance)", "jet"),
        (
            flow_region,
            "Flow Region Classification",
            "tab10",
        ),  # Cores categóricas bem diferenciadas
        (sdf2, "SDF2 (Wall Distance)", "jet"),
        (Ux, "Velocity Ux", "jet"),
        (Uy, "Velocity Uy", "jet"),
        (p, "Pressure", "jet"),
    ]

    for campo, titulo, cmap in campos:
        # Criar figura individual para cada campo
        fig, ax = plt.subplots(figsize=(8, 6))

        if titulo == "Flow Region Classification":
            # Força o uso de cores discretas em Flow Region
            cmap = plt.get_cmap("tab10")  # Alternativa: "Set1" para mais contraste
            im = ax.imshow(
                campo, cmap=cmap, origin="lower", aspect="auto", vmin=0, vmax=4
            )
        else:
            im = ax.imshow(campo, cmap=cmap, origin="lower", aspect="auto")

        ax.set_title(
            f"{titulo} - Amostra {sample_index}", fontsize=14, fontweight="bold"
        )
        ax.set_xlabel("X (grid points)")
        ax.set_ylabel("Y (grid points)")

        # Adiciona colorbar
        cbar = fig.colorbar(im, ax=ax, orientation="vertical", fraction=0.046, pad=0.04)
        cbar.set_label("Magnitude", fontsize=10)

        # Estatísticas do campo
        min_val, max_val, mean_val = campo.min(), campo.max(), campo.mean()
        text_info = f"Min: {min_val:.4f}\nMax: {max_val:.4f}\nMean: {mean_val:.4f}"
        ax.text(
            0.05,
            0.95,
            text_info,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(facecolor="white", alpha=0.7),
        )

        # Salvar cada figura na pasta `processed_data/visualizations/`
        filename = os.path.join(
            visualization_dir, f"sample_{sample_index}_{titulo.replace(' ', '_')}.png"
        )
        plt.savefig(filename, dpi=300)
        plt.close(fig)  # Fecha a figura para liberar memória

        print(f"📂 Imagem salva: {filename}")


if __name__ == "__main__":
    plot_sample()
