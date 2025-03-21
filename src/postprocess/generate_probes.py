import os
import shutil
import sys
import numpy as np
from postprocess.config import SYSTEM_PATH, BASE_PATH, X_MIN, X_MAX, NX, Y_MIN, Y_MAX, NY

PROBES_FILE_PATH = os.path.join(SYSTEM_PATH, "probes")

def clean_postprocessing():
    """Remove a pasta postProcessing para garantir um novo conjunto de dados."""
    postprocess_path = os.path.join(BASE_PATH, "postProcessing")
    
    if os.path.exists(postprocess_path):
        print(f"\n🗑️  Removendo pasta {postprocess_path} ...")
        shutil.rmtree(postprocess_path)
        print("✅ Pasta postProcessing removida com sucesso!\n")
    else:
        print("⚠️ Nenhuma pasta postProcessing encontrada para remover.\n")
def generate_probes():
    """Gera o arquivo probes para capturar dados em 100x100 pontos."""
    print("\n📄 Criando arquivo probes para OpenFOAM...\n")

    # Criando os pontos de amostragem
    x_values = np.linspace(X_MIN, X_MAX, NX)  # 100 pontos em X
    y_values = np.linspace(Y_MIN, Y_MAX, NY)  # 100 pontos em Y

    # Cabeçalho do arquivo probes
    probes_dict = """/*--------------------------------*- C++ -*----------------------------------*\\
| OpenFOAM: Probes Dict
\\*---------------------------------------------------------------------------*/

#includeEtc "caseDicts/postProcessing/probes/probes.cfg"

fields (U);
probeLocations
(
    (0 1 0)
    (1 0 0)
);





"""

    # Criar diretório system se não existir
    os.makedirs(SYSTEM_PATH, exist_ok=True)

    # Salvar o arquivo probes
    with open(PROBES_FILE_PATH, "w") as f:
        f.write(probes_dict)

    # print(f"✅ Arquivo '{PROBES_FILE_PATH}' gerado com sucesso!")
    # print(f"📄 Número de pontos gerados: {len(probe_lines)}\n")


import subprocess

def run_probes_postprocess():
    """Executa o postProcess para capturar os valores das sondas."""
    print("\n⚙️ Executando postProcess para capturar os valores das sondas...\n")
    
    case_path = BASE_PATH  # template-lam/

    try:
        subprocess.run(["postProcess", "-func", "probes", "-latestTime"], cwd=case_path, check=True)
        print("✅ postProcess concluído com sucesso!\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao executar postProcess: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    generate_probes()           # Gera o arquivo probes
    clean_postprocessing()      # Limpa a pasta postProcessing
    run_probes_postprocess()    # Executa postProcess para capturar os valores

