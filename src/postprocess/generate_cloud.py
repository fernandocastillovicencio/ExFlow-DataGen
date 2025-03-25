import os
import shutil
import sys
import numpy as np
import subprocess
from postprocess.config import SYSTEM_PATH, BASE_PATH, X_MIN, X_MAX, DX, Y_MIN, Y_MAX, DY, NPOINTS

CLOUD_FILE_PATH = os.path.join(SYSTEM_PATH, "cloud")
POSTPROCESS_PATH = os.path.join(BASE_PATH, "postProcessing", "cloud")

def get_latest_time():
    """Obtém o último time step presente na pasta postProcessing/cloud."""
    if not os.path.exists(POSTPROCESS_PATH):
        return None

    try:
        times = sorted([float(t) for t in os.listdir(POSTPROCESS_PATH) if t.replace(".", "").isdigit()])
        return str(int(times[-1])) if times else None
    except Exception as e:
        print(f"❌ ERRO ao detectar latestTime: {e}")
        return None

def clean_previous_cloud():
    """Remove apenas os arquivos antigos de cloud, mantendo a estrutura."""
    latest_time = get_latest_time()
    
    if latest_time:
        cloud_path = os.path.join(POSTPROCESS_PATH, latest_time)
        print(f"\n🗑️  Removendo arquivos antigos de cloud em {cloud_path} ...")
        shutil.rmtree(cloud_path)
        print("✅ Arquivos de cloud removidos!\n")
    else:
        print("⚠️ Nenhum resultado anterior encontrado para limpar.\n")

def generate_cloud():
    """Gera o arquivo cloud para capturar dados em uma grade 100x100 dentro do domínio."""
    print("\n📄 Criando arquivo cloud para OpenFOAM...\n")

    # Criar pontos no centro das células (evitando limites extremos)
    x_values = X_MIN + DX/2 + np.arange(NPOINTS) * DX
    y_values = Y_MIN + DY/2 + np.arange(NPOINTS) * DY

    # Construir a lista de coordenadas para cloud
    cloud_lines = []
    for x in x_values:
        for y in y_values:
            cloud_lines.append(f"    ({x:.6f} {y:.6f} 0)")

    # Cabeçalho do arquivo cloud
    cloud_dict = """/*--------------------------------*- C++ -*----------------------------------*\\
| OpenFOAM: Cloud Dict
\\*---------------------------------------------------------------------------*/

FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      cloud;
}

type                sets;
libs                (sampling);
interpolationScheme cell;
setFormat           raw;

writeControl        writeTime;

fields
(
    U
    p
);

sets
{
    ref_point
    {
        type    cloud;
        axis    xyz;
        points
(
""" + "\n".join(cloud_lines) + """
);
    }
}
"""

    # Criar diretório system se não existir
    os.makedirs(SYSTEM_PATH, exist_ok=True)

    # Salvar o arquivo cloud
    with open(CLOUD_FILE_PATH, "w") as f:
        f.write(cloud_dict)

    print(f"✅ Arquivo '{CLOUD_FILE_PATH}' gerado com sucesso!")
    print(f"📄 Número total de pontos gerados: {len(cloud_lines)}\n")

def run_cloud_postprocess():
    """Executa o postProcess no latestTime para capturar os valores dos pontos."""
    print("\n⚙️ Executando postProcess para capturar os valores dos pontos cloud...\n")
    
    case_path = BASE_PATH  # template-lam/

    try:
        subprocess.run(["postProcess", "-func", "cloud", "-latestTime"], cwd=case_path, check=True)
        print("✅ postProcess concluído com sucesso!\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao executar postProcess: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    generate_cloud()            # Gera o arquivo cloud
    clean_previous_cloud()      # Remove somente os arquivos antigos do cloud
    run_cloud_postprocess()     # Executa postProcess apenas no latestTime
