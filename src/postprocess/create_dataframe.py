import os
import numpy as np
import pandas as pd
from postprocess.config import SAMPLE_PATH, POSTPROCESS_PATH  # Caminho da pasta SAMPLE_PATH

def extract_x_from_filename(filename):
    """Extrai o valor de x do nome do arquivo, considerando 6 casas decimais corretamente."""
    identifier = filename.split("_")[0]  # Ex: 'xp3680000' ou 'xn0080000'
    
    sign = -1 if identifier.startswith("xn") else 1
    x_value = float(identifier[2:]) / 1000  # **Correção:** Convertendo corretamente para unidade desejada

    return sign * x_value

def load_sample_data():
    """Carrega todos os arquivos de SAMPLE_PATH e retorna um DataFrame consolidado."""
    
    if not os.path.exists(SAMPLE_PATH):
        print(f"❌ ERRO: Diretório {SAMPLE_PATH} não encontrado!")
        return None

    # Listar arquivos e ordenar com base no valor de x
    files = sorted(
        [f for f in os.listdir(SAMPLE_PATH) if f.endswith(".xy")],
        key=extract_x_from_filename
    )

    if not files:
        print(f"❌ ERRO: Nenhum arquivo .xy encontrado em {SAMPLE_PATH}!")
        return None

    data_list = []

    # Processar cada arquivo e extrair as colunas
    for file in files:
        file_path = os.path.join(SAMPLE_PATH, file)
        x_value = extract_x_from_filename(file)

        try:
            data = np.loadtxt(file_path)
            if data.ndim == 1:
                data = data.reshape(1, -1)  # Garantir formato 2D

            # Criar DataFrame com colunas nomeadas
            df = pd.DataFrame({
                "x": np.full(data.shape[0], x_value),  # Mesmo valor de x para todas as linhas
                "y": data[:, 0],  # Primeira coluna
                "p": data[:, 1],  # Segunda coluna
                "Ux": data[:, 2],  # Terceira coluna
                "Uy": data[:, 3],  # Quarta coluna
            })

            data_list.append(df)

        except Exception as e:
            print(f"❌ ERRO ao processar {file}: {e}")

    # Concatenar todos os DataFrames em um único
    final_df = pd.concat(data_list, ignore_index=True)

    print(f"✅ DataFrame criado com {len(final_df)} linhas e {len(final_df.columns)} colunas!")

    # Salvar o DataFrame na pasta postProcessing
    df_csv_path = os.path.join(POSTPROCESS_PATH, "sample_data.csv")
    df_npy_path = os.path.join(POSTPROCESS_PATH, "sample_data.npy")

    # Salvar os arquivos
    final_df.to_csv(df_csv_path, index=False)
    np.save(df_npy_path, final_df.to_numpy())

    print(f"✅ DataFrame salvo com sucesso na pasta postProcessing!")
    print(f"📂 CSV salvo em: {df_csv_path}")
    print(f"📂 NPY salvo em: {df_npy_path}")

    return final_df

if __name__ == "__main__":
    print("\n🔍 [DEBUG] Iniciando criação do DataFrame a partir dos arquivos sample...\n")
    df = load_sample_data()

    if df is not None:
        print(f"📊 [DEBUG] Exemplo de dados:\n{df.head()}")
        print(f"📊 [DEBUG] DataFrame contém {len(df)} linhas e {len(df.columns)} colunas.")
