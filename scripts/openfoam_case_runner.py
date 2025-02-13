import os
import logging
import subprocess
from modules.geometry_handler import get_geometry_folders, merge_stl_files
from modules.case_initializer import create_case_folders, copy_template
from modules.meshing_runner import run_meshing  # Importa o módulo de meshing

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/openfoam_case_runner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("OpenFOAMCaseRunner")

# Função para limpar a malha se já existir
def clean_mesh(case_folder):
    polyMesh_path = os.path.join(case_folder, "constant/polyMesh")
    
    if os.path.exists(polyMesh_path):
        logger.info(f"Limpando malha existente em {case_folder}")
        subprocess.run(["foamCleanPolyMesh"], cwd=case_folder, capture_output=True, text=True)
    else:
        logger.info(f"Nenhuma malha anterior encontrada para limpar em {case_folder}")

# Execução principal
if __name__ == "__main__":
    geometries = get_geometry_folders()[:2]  # Limita a apenas 2 geometrias para debugging

    for idx, geom in enumerate(geometries, start=1):  # Processa um caso por vez
        logger.info(f"Processando caso {idx}: {geom}")

        case_folder = create_case_folders(idx)

        # Verifica se a pasta já existe e remove para sobrescrever
        if os.path.exists(case_folder):
            logger.info(f"Removendo pasta existente: {case_folder}")
            subprocess.run(["rm", "-rf", case_folder], capture_output=True, text=True)

        os.makedirs(case_folder, exist_ok=True)  # Recria a pasta vazia

        geom_folder = f"cases/geometries/{geom}"

        # Copia arquivos necessários para meshing
        copy_template(case_folder, "system.cfmesh", "system")
        copy_template(case_folder, "constant.cfmesh", "constant")

        # Mescla arquivos STL
        merge_stl_files(idx, geom_folder)

        # Limpa malha se já existir
        clean_mesh(case_folder)

        # Executa meshing (inclui cartesianMesh, extrudeMesh e checkMesh)
        meshing_success = run_meshing(case_folder)

        if meshing_success:
            logger.info(f"Meshing finalizado com sucesso para {case_folder}. Iniciando próximo caso...")
        else:
            logger.warning(f"Meshing falhou para {case_folder}, pulando para o próximo caso.")
