import numpy as np
import os

# Diretório do pós-processamento
POSTPROCESS_DIR = "postProcessing/sample/latestTime"

# Arquivos extraídos do OpenFOAM
files = {
    "Ux": "sampleGrid_U.xy",
    "Uy": "sampleGrid_U.xy",
    "p": "sampleGrid_p.xy"
}

# Criar diretório de saída
OUTPUT_DIR = "processed_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for key, filename in files.items():
    filepath = os.path.join(POSTPROCESS_DIR, filename)
    if os.path.exists(filepath):
        print(f"🔄 Convertendo {filename} para {key}.npy ...")
        data = np.loadtxt(filepath)  # Carregar os valores do OpenFOAM
        np.save(os.path.join(OUTPUT_DIR, f"{key}.npy"), data[:, -1])  # Salvar apenas os valores
        print(f"✅ Salvo: {OUTPUT_DIR}/{key}.npy")
    else:
        print(f"❌ Arquivo não encontrado: {filepath}")
