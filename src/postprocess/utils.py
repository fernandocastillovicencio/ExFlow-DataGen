import os
import shutil
from postprocess.config import TEMPLATE_DIR, OUTPUT_DIR, U_FILE_NAME, LOG_FILE_NAME
from postprocess.generate_cloud import main as run_generate_cloud

def get_case_dirs():
    """ Retorna uma lista de todas as pastas de casos dentro de OUTPUT_DIR """
    if not os.path.exists(OUTPUT_DIR):
        return []

    return [os.path.join(OUTPUT_DIR, d) for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))]

def is_simulation_done(case_dir):
    log_path = os.path.join(case_dir, LOG_FILE_NAME)

    if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
        return False

    time_dirs = [d for d in os.listdir(case_dir) if d.isdigit()]
    return bool(time_dirs)

def run_case(U):
    """Executa SimpleFoam apenas se necessário."""
    U_INT = int(U)
    U_DEC = int((U * 10) % 10)
    CASE_DIR = os.path.join(OUTPUT_DIR, f"U{U_INT}{U_DEC}")

    if is_simulation_done(CASE_DIR):
        print(f"⚠️ Simulação já concluída para {CASE_DIR}, pulando execução.")
        return

    print(f"\n⚙️ Iniciando simulação dentro de {CASE_DIR}...\n")
    log_file = os.path.join(CASE_DIR, LOG_FILE_NAME)

    with open(log_file, "w") as log:
        os.system(f"cd {CASE_DIR} && simpleFoam > log.simpleFoam 2>&1")

    print(f"✅ Simulação concluída para {CASE_DIR}")

def run_postprocess(case_dir):
    """Executa o pós-processamento dentro do diretório do caso."""
    print(f"\n🔍 Iniciando pós-processamento para {case_dir}...\n")

    try:
        run_generate_cloud(case_dir)
        print(f"✅ Pós-processamento concluído para {case_dir}")
    except Exception as e:
        print(f"❌ ERRO ao processar {case_dir}: {e}")
