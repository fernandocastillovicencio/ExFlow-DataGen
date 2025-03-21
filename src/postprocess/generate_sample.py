import os
import sys
import re
import shutil
import numpy as np
import subprocess
from postprocess.config import SYSTEM_PATH, SAMPLE_FILE_PATH, X_MIN,NX, X_MAX, DX, NY, Y_MIN, Y_MAX, DY, BASE_PATH

POSTPROCESS_DIR = os.path.join(BASE_PATH, "postProcessing")

def generate_sample():
    """Gera o arquivo sample dentro do diretório system/ para OpenFOAM."""
    print("\n📄 Criando arquivo sample para OpenFOAM...\n")

    # Criando os pontos centrais das células em X usando DX
    x_centers = np.array([X_MIN + ((2 * i + 1) / 2) * DX for i in range(NX)])


    # Cabeçalho do arquivo sample
    sample_dict = """/*--------------------------------*- C++ -*----------------------------------*\\
| OpenFOAM: Sample Dict
\\*---------------------------------------------------------------------------*/

FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      sample;
}

type            sets;
libs            (sampling);
interpolationScheme cellPointFace;
setFormat       raw;

fields          (U p);

sets
(
"""

    # Criando os blocos ao longo de X
    block_lines = []
    for x in x_centers:
        block_name = f"xp{int(abs(x) * 1e3):04d}" if x >= 0 else f"xn{int(abs(x) * 1e3):04d}"

        block_lines.append(f"""    {block_name}
    {{
        type        uniform;
        axis        y;
        start       ({x} {Y_MIN+DY/2} 0);
        end         ({x} {Y_MAX-DY/2} 0);
        nPoints     {NY};
    }}\n""")

    # Verificar se blocos foram gerados
    if not block_lines:
        print("❌ ERRO: Nenhum bloco foi gerado para o arquivo sample!")
        sys.exit(1)

    # Adiciona os blocos ao arquivo
    sample_dict += "".join(block_lines)
    sample_dict += ");\n"  # Fechamento correto do arquivo

    # Criar diretório system se não existir
    os.makedirs(SYSTEM_PATH, exist_ok=True)

    # Salvar o arquivo sample
    with open(SAMPLE_FILE_PATH, "w") as f:
        f.write(sample_dict)

    print(f"✅ Arquivo '{SAMPLE_FILE_PATH}' gerado com sucesso!")
    print(f"📄 Número de blocos gerados: {len(block_lines)}\n")


# -------------------------------------------------------- #
def verify_sample():
    """Verifica se os nomes dos blocos dentro do arquivo sample estão corretos."""
    print("\n🔍 Verificando o arquivo sample...\n")

    if not os.path.exists(SAMPLE_FILE_PATH):
        print(f"❌ ERRO: O arquivo sample não foi encontrado em {SAMPLE_FILE_PATH}")
        sys.exit(1)

    with open(SAMPLE_FILE_PATH, "r") as f:
        content = f.readlines()

    block_names = []
    for i in range(len(content) - 1):  # Percorre as linhas
        line = content[i].strip()
        next_line = content[i + 1].strip() if i + 1 < len(content) else ""

        # Verifica se a linha contém "xpXXX" ou "xnXXX" e se a próxima linha contém "{"
        match = re.match(r"(xp\d{3}|xn\d{3})", line) and next_line == "{"
        if match:
            block_names.append(line)

    if block_names:
        print(f"✅ {len(block_names)} blocos detectados no arquivo sample.")
        print(f"🔹 Exemplo de blocos: {block_names[:5]} ...")  # Exibe apenas os primeiros blocos
    else:
        print("❌ ERRO: Nenhum bloco foi encontrado no arquivo sample.")
        print("📌 DICA: Verifique se os nomes dos blocos estão formatados corretamente no arquivo.")
        sys.exit(1)

    print("\n✅ Verificação do sample concluída.\n")


# -------------------------------------------------------- #
def find_latest_time():
    """Detecta automaticamente o latestTime dentro de postProcessing/."""
    if not os.path.exists(POSTPROCESS_DIR):
        print("❌ ERRO: Diretório postProcessing/ não encontrado.")
        return None

    time_dirs = [d for d in os.listdir(POSTPROCESS_DIR) if re.match(r"^\d+(\.\d+)?$", d)]
    if not time_dirs:
        print("⚠️ Nenhuma pasta de tempo encontrada dentro de postProcessing/.")
        return None

    latest_time = max(time_dirs, key=float)  # Encontra o maior número (latestTime)
    return os.path.join(POSTPROCESS_DIR, latest_time)

def clean_latest_time():
    """Apaga automaticamente a pasta correspondente ao latestTime."""
    latest_time_path = find_latest_time()
    if latest_time_path:
        print(f"\n🗑️  Removendo pasta latestTime: {latest_time_path} ...")
        shutil.rmtree(latest_time_path)
        print("✅ Pasta latestTime removida com sucesso!\n")
    else:
        print("⚠️ Nenhuma pasta latestTime para remover.\n")

def run_postprocess():
    """Executa o OpenFOAM postProcess dentro do diretório do case."""
    print("\n⚙️ Executando postProcess para gerar os arquivos .xy...\n")
    
    case_path = BASE_PATH  # template-lam/
    
    if not os.path.exists(os.path.join(case_path, "system/controlDict")):
        print(f"❌ ERRO: O arquivo controlDict não foi encontrado em {case_path}/system/")
        sys.exit(1)

    try:
        subprocess.run(["postProcess", "-func", "sample", "-latestTime"], cwd=case_path, check=True)
        print("✅ postProcess concluído com sucesso!\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao executar postProcess: {e}\n")
        sys.exit(1)

def debug_sample_file():
    """Exibe as primeiras linhas do arquivo sample para depuração."""
    print("\n📄 Exibindo as primeiras 20 linhas do arquivo sample para verificação:\n")

    if not os.path.exists(SAMPLE_FILE_PATH):
        print(f"❌ ERRO: O arquivo sample não foi encontrado em {SAMPLE_FILE_PATH}")
        sys.exit(1)

    with open(SAMPLE_FILE_PATH, "r") as f:
        lines = f.readlines()
    
    for line in lines[:20]:  # Exibe apenas as primeiras 20 linhas
        print(line.strip())  

    print("\n✅ Fim da visualização do arquivo sample.\n")

if __name__ == "__main__":
    generate_sample()    # Gera o arquivo sample
    clean_latest_time()  # Apaga os dados antigos antes de executar postProcess
    run_postprocess()    # Executa postProcess para gerar os arquivos
    debug_sample_file()  # Exibe o conteúdo do sample para análise
    verify_sample()      # Verifica os blocos gerados
