import os
from config import CLOUD_PATH

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
