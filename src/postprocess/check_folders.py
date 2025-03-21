import os
import sys

import os
import sys

# Adiciona o caminho da pasta `src` ao sys.path para que o Python reconheça os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.postprocess.config import BASE_PATH, SYSTEM_PATH, POSTPROCESS_PATH, OUTPUT_NPY_PATH

def check_folders():
    """Verifica se as pastas necessárias para o pós-processamento existem."""
    print("\n🔍 Verificando a estrutura de diretórios...\n")

    # Dicionário com os caminhos a serem verificados
    folders = {
        "Base do Template OpenFOAM": BASE_PATH,
        "Pasta de Configuração (system/)": SYSTEM_PATH,
        "Pasta de Dados do OpenFOAM (postProcessing/)": POSTPROCESS_PATH,
        "Pasta de Saída para NPY": os.path.dirname(OUTPUT_NPY_PATH)
    }

    # Verificando se cada pasta existe
    for name, path in folders.items():
        if os.path.exists(path):
            print(f"✅ {name}: Encontrada ({path})")
        else:
            print(f"❌ {name}: NÃO ENCONTRADA! ({path})")
            print("🔴 ERRO: A pasta é necessária para continuar.")
            sys.exit(1)  # Encerra o script com erro

    print("\n✅ Todas as pastas necessárias foram encontradas.\n")

if __name__ == "__main__":
    check_folders()
