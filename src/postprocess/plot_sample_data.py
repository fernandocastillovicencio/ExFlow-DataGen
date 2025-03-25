import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from postprocess.config import CLOUD_PATH, PLOT_PATH, DX, DY, X_MIN, X_MAX, Y_MIN, Y_MAX  # Importando configurações

def load_cloud_data():
    """Carrega o arquivo de dados mais recente de cloud e retorna um DataFrame."""
    
    # Identificar o latestTime
    cloud_dir = os.path.join(CLOUD_PATH)
    latest_time = max([float(d) for d in os.listdir(cloud_dir) if d.replace(".", "").isdigit()])
    latest_time_dir = os.path.join(cloud_dir, str(int(latest_time)))

    file_path = os.path.join(latest_time_dir, "ref_point_p_U.xy")

    if not os.path.exists(file_path):
        print(f"❌ ERRO: Arquivo {file_path} não encontrado!")
        return None

    # Carregar os dados
    try:
        data = np.loadtxt(file_path)
        df = pd.DataFrame({
            "x": data[:, 0],
            "y": data[:, 1],
            "p": data[:, 3],
            "Ux": data[:, 4],
            "Uy": data[:, 5]
        })

        return df

    except Exception as e:
        print(f"❌ ERRO ao processar o arquivo {file_path}: {e}")
        return None

def plot_fields(df):
    """Gera os plots dos campos Ux, Uy e p desenhando retângulos de tamanho DX x DY."""

    # Criar figure e subplots
    # Definir a proporção baseada na extensão dos eixos X e Y
    fig_width = 10  # Largura base da figura (ajustável)
    aspect_ratio = (Y_MAX - Y_MIN) / (X_MAX - X_MIN)
    fig_height = fig_width * aspect_ratio  # Ajustar altura proporcionalmente

    # Criar figure e subplots com tamanho ajustado
    fig, axes = plt.subplots(3, 1, figsize=(fig_width, fig_height*2.6 ), constrained_layout=True)


    fields = ["Ux", "Uy", "p"]
    titles = ["Velocidade Ux", "Velocidade Uy", "Pressão (p)"]
    cmap = "jet"  # Usar cmap jet para melhor visualização

    for ax, field, title in zip(axes, fields, titles):
        norm = plt.Normalize(df[field].min(), df[field].max())  # Normalização das cores
        cmap_instance = plt.get_cmap(cmap)

        for _, row in df.iterrows():
            color = cmap_instance(norm(row[field]))  # Cor baseada no valor do campo
            rect = patches.Rectangle(
                (row["x"] - DX / 2, row["y"] - DY / 2),  # Canto inferior esquerdo do retângulo
                DX, DY,  # Largura e altura
                linewidth=0,
                edgecolor=None,
                facecolor=color
            )
            ax.add_patch(rect)

        ax.set_xlim(df["x"].min() - DX, df["x"].max() + DX)
        ax.set_ylim(df["y"].min() - DY, df["y"].max() + DY)
        ax.set_title(title)
        ax.set_xlabel("Posição X")
        ax.set_ylabel("Posição Y")

        # Adiciona barra de cores
        sm = plt.cm.ScalarMappable(cmap=cmap_instance, norm=norm)
        sm.set_array([])
        fig.colorbar(sm, ax=ax, label=title)

    # Salvar a figura
    os.makedirs(PLOT_PATH, exist_ok=True)
    output_file = os.path.join(PLOT_PATH, "cloud_fields_rectangles.png")
    plt.savefig(output_file, dpi=300)
    print(f"✅ Plot salvo em {output_file}")

if __name__ == "__main__":
    print("\n🔍 [DEBUG] Iniciando criação do plot a partir dos arquivos cloud...\n")
    df = load_cloud_data()

    if df is not None:
        plot_fields(df)
