import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from postprocess.config import DX, DY, X_MIN, X_MAX, Y_MIN, Y_MAX

def load_cloud_data(case_dir):
    """Carrega o arquivo de dados mais recente de cloud dentro de um caso específico e retorna um DataFrame."""
    
    cloud_path = os.path.join(case_dir, "postProcessing", "cloud")

    if not os.path.exists(cloud_path):
        print(f"❌ ERRO: Diretório {cloud_path} não encontrado!")
        return None

    # Encontrar o último tempo salvo
    time_dirs = [d for d in os.listdir(cloud_path) if d.isdigit()]
    if not time_dirs:
        print(f"❌ ERRO: Nenhuma pasta de tempo encontrada em {cloud_path}")
        return None

    latest_time = max(map(int, time_dirs))
    latest_time_dir = os.path.join(cloud_path, str(latest_time))

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

def plot_fields(case_dir):
    """Gera e salva os plots dos campos Ux, Uy e p dentro do diretório do caso."""

    df = load_cloud_data(case_dir)
    if df is None:
        return

    # Criar diretório para salvar os plots dentro do caso específico
    plot_path = os.path.join(case_dir, "plots")
    os.makedirs(plot_path, exist_ok=True)

    # Definir dimensões da figura
    fig_width = 10  
    aspect_ratio = (Y_MAX - Y_MIN) / (X_MAX - X_MIN)
    fig_height = fig_width * aspect_ratio  

    # Criar figura e subplots ajustados
    fig, axes = plt.subplots(3, 1, figsize=(fig_width, fig_height*2.6), constrained_layout=True)

    fields = ["Ux", "Uy", "p"]
    titles = ["Velocidade Ux", "Velocidade Uy", "Pressão (p)"]
    cmap = "jet"

    for ax, field, title in zip(axes, fields, titles):
        norm = plt.Normalize(df[field].min(), df[field].max())
        cmap_instance = plt.get_cmap(cmap)

        for _, row in df.iterrows():
            color = cmap_instance(norm(row[field]))
            rect = patches.Rectangle(
                (row["x"] - DX / 2, row["y"] - DY / 2),
                DX, DY,
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

    # Salvar a figura no diretório do caso
    output_file = os.path.join(plot_path, "cloud_fields_rectangles.png")
    plt.savefig(output_file, dpi=300)
    print(f"✅ Plot salvo em {output_file}")

def main(case_dir):
    """Executa a geração de gráficos de amostragem para um caso específico."""
    plot_fields(case_dir)
