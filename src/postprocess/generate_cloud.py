import os
import numpy as np
import subprocess
import sys
from postprocess.config import X_MIN, X_MAX, DX, Y_MIN, Y_MAX, DY, NPOINTS

def generate_cloud(case_dir):
    """Gera o arquivo cloud dentro do diretório do caso especificado."""
    print(f"\n📄 Criando arquivo cloud para {case_dir}...\n")

    system_path = os.path.join(case_dir, "system")
    cloud_file_path = os.path.join(system_path, "cloud")

    # Criar pontos no centro das células
    x_values = X_MIN + DX / 2 + np.arange(NPOINTS) * DX
    y_values = Y_MIN + DY / 2 + np.arange(NPOINTS) * DY

    # Construir a lista de coordenadas para cloud
    cloud_lines = [f"    ({x:.6f} {y:.6f} 0)" for x in x_values for y in y_values]

    # Cabeçalho do arquivo cloud
    cloud_dict = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| OpenFOAM: Cloud Dict
\\*---------------------------------------------------------------------------*/

FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      cloud;
}}

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
{{
    ref_point
    {{
        type    cloud;
        axis    xyz;
        points
(
{chr(10).join(cloud_lines)}
);
    }}
}}
"""

    os.makedirs(system_path, exist_ok=True)

    # Salvar o arquivo cloud dentro da pasta do caso
    with open(cloud_file_path, "w") as f:
        f.write(cloud_dict)

    print(f"✅ Arquivo '{cloud_file_path}' gerado com sucesso!")

def run_cloud_postprocess(case_dir):
    """Executa o postProcess dentro do caso."""
    print(f"\n⚙️ Executando postProcess em {case_dir}...\n")

    try:
        subprocess.run(["postProcess", "-func", "cloud", "-latestTime"], cwd=case_dir, check=True)
        print(f"✅ Pós-processamento concluído com sucesso em {case_dir}!\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao executar postProcess em {case_dir}: {e}")
        sys.exit(1)

def main(case_dir):
    """Executa a geração do arquivo cloud e o pós-processamento no diretório especificado."""
    generate_cloud(case_dir)
    run_cloud_postprocess(case_dir)
