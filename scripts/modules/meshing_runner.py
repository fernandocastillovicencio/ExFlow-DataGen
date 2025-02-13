import os
import subprocess
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/meshing_runner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MeshingRunner")

def run_command(command, case_folder, log_file):
    """
    Executa um comando dentro do diretório do caso e salva o log.
    Retorna True se o comando for bem-sucedido, False caso contrário.
    """
    log_path = os.path.join(case_folder, log_file)
    logger.info(f"Executando {' '.join(command)} em {case_folder}")

    try:
        with open(log_path, "w") as log:
            result = subprocess.run(command, cwd=case_folder, stdout=log, stderr=log, text=True)

        if result.returncode != 0:
            logger.error(f"Erro ao executar {' '.join(command)}. Verifique {log_path} para detalhes.")
            return False

        logger.info(f"Concluído: {' '.join(command)}. Log salvo em {log_path}")
        return True

    except Exception as e:
        logger.error(f"Falha ao executar {' '.join(command)}: {e}")
        return False

def run_meshing(case_folder):
    """
    Executa cartesianMesh, extrudeMesh e checkMesh no diretório do caso.
    Registra logs para cada etapa.
    """

    # Executa cartesianMesh
    if not run_command(["cartesianMesh"], case_folder, "log.cartesianMesh"):
        return False

    # Executa extrudeMesh
    if not run_command(["extrudeMesh"], case_folder, "log.extrudeMesh"):
        return False

    # Executa checkMesh
    if not run_command(["checkMesh"], case_folder, "log.checkMesh"):
        return False

    return True  # Meshing concluído com sucesso
