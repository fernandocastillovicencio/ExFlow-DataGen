import os
import numpy as np
from postprocess.config import SAMPLE_PATH, NPOINTS, Y_MIN, Y_MAX, DY  # Extraído de config.py

def get_sample_files():
    """Lista os arquivos dentro de postProcessing/sample/5/."""

    if not os.path.exists(SAMPLE_PATH):
        print(f"❌ ERRO: Diretório {SAMPLE_PATH} não encontrado!")
        return None

    # Listar apenas arquivos com extensão .xy
    files = sorted([f for f in os.listdir(SAMPLE_PATH) if f.endswith(".xy")])

    if not files:
        print(f"❌ ERRO: Nenhum arquivo .xy encontrado em {SAMPLE_PATH}!")
        return None

    print(f"✅ [DEBUG] Arquivos detectados ({len(files)}): {files}")
    return SAMPLE_PATH, files

def count_lines_in_files(sample_path, files):
    """Conta o número de linhas de dados em cada arquivo e compara com NPOINTS."""
    print("\n📊 [DEBUG] Contando linhas de dados nos arquivos...\n")

    for file in files:
        file_path = os.path.join(sample_path, file)
        try:
            data = np.loadtxt(file_path)
            num_rows = data.shape[0] if data.ndim > 1 else 1  # Se for um único valor, considera 1 linha
            
            status = "✅ OK" if num_rows == NPOINTS else f"⚠️ Diferença de {NPOINTS - num_rows} pontos"
            print(f"📄 [DEBUG] Arquivo: {file} | Linhas de dados: {num_rows} | {status}")

        except Exception as e:
            print(f"❌ ERRO ao processar {file}: {e}")
def fix_missing_points(sample_path, files):
    """Verifica e corrige arquivos que possuem menos pontos que NPOINTS."""
    print("\n🛠️ [DEBUG] Verificando e corrigindo arquivos com pontos faltantes...\n")

    for file in files:
        file_path = os.path.join(sample_path, file)
        try:
            data = np.loadtxt(file_path)  # Carregar dados do arquivo
            
            # Se for uma linha só e não um array, transformar em matriz 2D
            if data.ndim == 1:
                data = data.reshape(1, -1)

            num_rows = data.shape[0]
            existing_y_values = set(np.round(data[:, 0], 3))  # Usar set para evitar duplicatas

            if num_rows == NPOINTS:
                print(f"✅ [DEBUG] Arquivo {file} já está correto. Nenhuma alteração necessária.")
                continue  # Pula para o próximo arquivo
            
            # Determinar os valores de Y esperados
            # Criando os pontos centrais das células em Y usando DY
            expected_y_values = np.array([Y_MIN + ((2 * i + 1) / 2) * DY for i in range(NPOINTS)])


            # Encontrar os valores de Y que estão faltando
            missing_y = [y for y in expected_y_values if round(y, 3) not in existing_y_values]


            if missing_y:
                print(f"⚠️ [DEBUG] Corrigindo {len(missing_y)} pontos ausentes em {file}...")

                # Criar linhas de preenchimento (Y correto, resto 0.000000)
                missing_rows = np.array([[y, 0.0, 0.0, 0.0, 0.0] for y in missing_y])

                # Concatenar e ordenar pelo valor de Y
                corrected_data = np.vstack((data, missing_rows))
                corrected_data = corrected_data[np.argsort(corrected_data[:, 0])]  # Ordenar por Y
                
                # Salvar o arquivo corrigido
                np.savetxt(file_path, corrected_data, fmt="%.6f", delimiter=" ")

                print(f"✅ [DEBUG] Arquivo {file} corrigido e salvo.")

        except Exception as e:
            print(f"❌ ERRO ao processar {file}: {e}")

def verify_y_sequence(file_path, dy, tolerance=0.01):
    """Verifica se os valores da coluna Y estão em sequência correta com espaçamento aproximadamente igual a dy."""
    try:
        data = np.loadtxt(file_path)
        if data.ndim == 1:
            data = data.reshape(1, -1)  # Caso o arquivo tenha apenas uma linha

        y_values = data[:, 0]  # Extraindo os valores de Y
        y_diffs = np.diff(y_values)  # Diferença entre valores consecutivos

        for i, diff in enumerate(y_diffs):
            if abs(diff - dy) > tolerance * dy:
                print(f"⚠️ ALERTA: Espaçamento irregular detectado no arquivo {file_path} na linha {i+1}")
                print(f"    ➝ Diferença encontrada: {diff:.6f}, Esperado: ~{dy:.6f}")

    except Exception as e:
        print(f"❌ ERRO ao processar {file_path}: {e}")



if __name__ == "__main__":
    print("\n🔍 [DEBUG] Iniciando verificação e correção de pontos ausentes...\n")
    
    result = get_sample_files()
    if result:
        POSTPROCESS_PATH, files = result

        # 🔧 Corrigir arquivos com pontos ausentes
        fix_missing_points(POSTPROCESS_PATH, files)

        # 🔍 Verificar sequência correta de Y
        for file in files:
            file_path = os.path.join(POSTPROCESS_PATH, file)
            verify_y_sequence(file_path, dy=DY)

        print("\n✅ [DEBUG] Correção e verificação concluídas.")
    else:
        print("❌ ERRO: Não foi possível encontrar arquivos sample.")

