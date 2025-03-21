import os
from postprocess.config import POSTPROCESS_PATH  # Extraído de config.py

def get_sample_files():
    """Lista os arquivos dentro de postProcessing/sample/5/."""

    if not os.path.exists(POSTPROCESS_PATH):
        print(f"❌ ERRO: Diretório {POSTPROCESS_PATH} não encontrado!")
        return None

    # Listar apenas arquivos com extensão .xy
    files = sorted([f for f in os.listdir(POSTPROCESS_PATH) if f.endswith(".xy")])

    if not files:
        print(f"❌ ERRO: Nenhum arquivo .xy encontrado em {POSTPROCESS_PATH}!")
        return None

    print(f"✅ [DEBUG] Arquivos detectados ({len(files)}): {files}")
    return POSTPROCESS_PATH, files


if __name__ == "__main__":
    print("\n🔍 [DEBUG] Iniciando detecção de arquivos sample...\n")

    result = get_sample_files()

    if result:
        POSTPROCESS_PATH, files = result
        print(f"✅ [DEBUG] Pasta correta detectada: {POSTPROCESS_PATH}")
        print(f"✅ [DEBUG] Total de arquivos encontrados: {len(files)}")
    else:
        print("❌ ERRO: Não foi possível encontrar arquivos sample.")
