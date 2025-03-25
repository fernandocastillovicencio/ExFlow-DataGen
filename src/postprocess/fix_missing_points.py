import os
import numpy as np
from postprocess.config import CLOUD_PATH, X_MIN, X_MAX, Y_MIN, Y_MAX, DX, DY, NPOINTS  # Importando configurações

def get_latest_time():
    """Identifica o maior número de tempo dentro da pasta postProcessing/cloud/."""
    if not os.path.exists(CLOUD_PATH):
        print(f"❌ ERRO: Diretório {CLOUD_PATH} não encontrado!")
        return None

    time_dirs = [d for d in os.listdir(CLOUD_PATH) if d.isdigit()]
    if not time_dirs:
        print("❌ ERRO: Nenhuma pasta de tempo encontrada em postProcessing/cloud/")
        return None

    latest_time = max(map(int, time_dirs))  # Encontrar o maior número de tempo
    latest_path = os.path.join(CLOUD_PATH, str(latest_time))

    return latest_path

def fix_missing_cloud_points():
    """Verifica e corrige pontos ausentes no arquivo de amostragem cloud."""
    latest_path = get_latest_time()
    if latest_path is None:
        return

    file_path = os.path.join(latest_path, "ref_point_p_U.xy")  # Nome fixo do arquivo
    if not os.path.exists(file_path):
        print(f"❌ ERRO: Arquivo {file_path} não encontrado!")
        return

    print(f"📂 [DEBUG] Processando arquivo: {file_path}")

    # Carregar dados existentes
    data = np.loadtxt(file_path)

    if data.ndim == 1:
        data = data.reshape(1, -1)  # Garantir formato 2D

    # Extração das colunas x, y, z, p, Ux, Uy, Uz
    x_values = np.round(data[:, 0], 6)
    y_values = np.round(data[:, 1], 6)

    # Criar listas dos pontos esperados
    expected_x = np.round([X_MIN + (2 * i + 1) / 2 * DX for i in range(NPOINTS)], 6)
    expected_y = np.round([Y_MIN + (2 * i + 1) / 2 * DY for i in range(NPOINTS)], 6)

    # Criar um conjunto de pares existentes (x, y)
    existing_points = set(zip(x_values, y_values))

    # Verificar quais pontos estão faltando
    missing_points = []
    for x in expected_x:
        for y in expected_y:
            if (x, y) not in existing_points:
                missing_points.append([x, y, 0.0, 0.0, 0.0, 0.0, 0.0])  # Adicionar linha vazia

    if missing_points:
        print(f"⚠️ [DEBUG] Adicionando {len(missing_points)} pontos ausentes...")

        # Concatenar os dados existentes com os pontos ausentes
        corrected_data = np.vstack((data, missing_points))
        corrected_data = corrected_data[np.lexsort((corrected_data[:, 1], corrected_data[:, 0]))]  # Ordenação por x e y

        # Salvar o arquivo corrigido
        np.savetxt(file_path, corrected_data, fmt="%.6f", delimiter=" ")

        print(f"✅ [DEBUG] Arquivo corrigido e salvo: {file_path}")

    else:
        print("✅ [DEBUG] Nenhum ponto ausente encontrado. Nenhuma modificação necessária.")

if __name__ == "__main__":
    print("\n🔍 [DEBUG] Iniciando verificação e correção dos pontos de amostragem cloud...\n")
    fix_missing_cloud_points()
