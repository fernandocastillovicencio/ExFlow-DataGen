import os
import logging
import subprocess
from modules.geometry_handler import get_geometry_folders, merge_stl_files
from modules.case_initializer import create_case_folders, copy_template
from modules.meshing_runner import run_meshing  # Importa o módulo de meshing
from modules.boundary_fixer import fix_boundary  # Importa o módulo para corrigir o arquivo boundary

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
    """
    Remove malhas existentes no diretório do caso antes de rodar um novo meshing.
    Executa o comando `foamCleanPolyMesh` caso o diretório de malha já exista.
    """
    polyMesh_path = os.path.join(case_folder, "constant/polyMesh")
    
    if os.path.exists(polyMesh_path):
        logger.info(f"Limpando malha existente em {case_folder}")
        subprocess.run(["foamCleanPolyMesh"], cwd=case_folder, capture_output=True, text=True)
    else:
        logger.info(f"Nenhuma malha anterior encontrada para limpar em {case_folder}")

# Execução principal
if __name__ == "__main__":
    # Obtém a lista de geometrias, limitando a apenas 2 para debugging
    geometries = get_geometry_folders()[:2]  

    for idx, geom in enumerate(geometries, start=1):  # Processa um caso por vez
        logger.info(f"Processando caso {idx}: {geom}")

        case_folder = create_case_folders(idx)

        # Verifica se a pasta já existe e remove para sobrescrever
        if os.path.exists(case_folder):
            logger.info(f"Removendo pasta existente: {case_folder}")
            subprocess.run(["rm", "-rf", case_folder], capture_output=True, text=True)

        os.makedirs(case_folder, exist_ok=True)  # Recria a pasta vazia

        # Define o caminho da geometria correspondente ao caso
        geom_folder = f"cases/geometries/{geom}"

        # Copia os arquivos necessários do template para configurar o caso
        copy_template(case_folder, "system.cfmesh", "system")
        copy_template(case_folder, "constant.cfmesh", "constant")

        # Mescla arquivos STL da geometria para o caso
        merge_stl_files(idx, geom_folder)

        # Limpa malha se já existir para evitar conflitos
        clean_mesh(case_folder)

        # Executa o processo de malha: cartesianMesh → extrudeMesh → checkMesh
        meshing_success = run_meshing(case_folder)

        if meshing_success:
            logger.info(f"Meshing finalizado com sucesso para {case_folder}.")
            
            # Corrigir o arquivo boundary após a malha ser gerada
            logger.info(f"Corrigindo arquivo boundary em {case_folder}")
            boundary_fixed = fix_boundary(case_folder)

            if boundary_fixed:
                logger.info("Boundary corrigido com sucesso.")
            else:
                logger.warning("Falha ao corrigir boundary.")

        else:
            logger.warning(f"Meshing falhou para {case_folder}, pulando para o próximo caso.")
