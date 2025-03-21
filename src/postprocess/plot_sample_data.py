import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from postprocess.config import DX, DY, POSTPROCESS_PATH

# Caminho dos arquivos de saída
output_dir = os.path.join(POSTPROCESS_PATH, "figures")
os.makedirs(output_dir, exist_ok=True)

# Carregar os dados do DataFrame consolidado
df_path = os.path.join(POSTPROCESS_PATH, "sample_data.csv")
if not os.path.exists(df_path):
    raise FileNotFoundError(f"❌ ERRO: Arquivo {df_path} não encontrado!")

df = pd.read_csv(df_path)

def plot_field(df, field, title, filename, cmap="coolwarm"):
    """
    Plota e salva um mapa de calor para um campo específico (Ux, Uy, ou p).
    
    Parâmetros:
        df (pd.DataFrame): DataFrame com os dados.
        field (str): Nome da coluna a ser plotada ('Ux', 'Uy' ou 'p').
        title (str): Título do gráfico.
        filename (str): Nome do arquivo de saída.
        cmap (str): Colormap do matplotlib.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(title)
    ax.set_xlabel("Posição X")
    ax.set_ylabel("Posição Y")

    # Criar retângulos para cada ponto do DataFrame
    for _, row in df.iterrows():
        rect = patches.Rectangle(
            (row["x"], row["y"]),  # Posição do canto inferior esquerdo
            DX, DY,  # Tamanho do retângulo
            facecolor=plt.cm.get_cmap(cmap)(row[field]),  # Cor proporcional ao valor do campo
            edgecolor="none"
        )
        ax.add_patch(rect)

    # Ajustar limites do gráfico
    ax.set_xlim(df["x"].min(), df["x"].max())
    ax.set_ylim(df["y"].min(), df["y"].max())

    # Salvar a figura no diretório de saída
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path, dpi=300)
    plt.close(fig)

    print(f"✅ Imagem salva: {save_path}")

if __name__ == "__main__":
    print("\n🔍 [DEBUG] Iniciando criação dos mapas de calor...\n")

    # Criar os três mapas de calor e salvar como PNG
    plot_field(df, "Ux", "Campo de Velocidade Ux", "Ux_field.png")
    plot_field(df, "Uy", "Campo de Velocidade Uy", "Uy_field.png")
    plot_field(df, "p", "Campo de Pressão", "Pressure_field.png")

    print("✅ Todas as imagens foram geradas e salvas com sucesso!")
