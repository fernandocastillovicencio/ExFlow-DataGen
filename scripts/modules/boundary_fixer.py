import os
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/boundary_fixer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("BoundaryFixer")

def fix_boundary(case_folder):
    """
    Corrige o arquivo constant/polyMesh/boundary após a geração da malha.
    """
    boundary_file = os.path.join(case_folder, "constant/polyMesh/boundary")
    backup_file = boundary_file + ".bak"

    if not os.path.exists(boundary_file):
        logger.warning(f"Arquivo boundary não encontrado em {case_folder}. Nenhuma modificação aplicada.")
        return False

    # Criar backup antes da modificação
    if not os.path.exists(backup_file):
        os.system(f"cp {boundary_file} {backup_file}")
        logger.info(f"Backup do boundary criado: {backup_file}")

    # Ler o arquivo boundary
    with open(boundary_file, "r") as file:
        lines = file.readlines()

    # Dicionário de tipos corretos de patches no OpenFOAM
    boundary_types = {
        "inlet": "patch",
        "outlet": "patch",
        "upper": "patch",
        "lower": "patch",
        "front": "empty",
        "back": "empty",
        "obstacle": "wall"
    }

    corrected_lines = []
    inside_patch = False
    current_patch = ""

    # Corrigir os tipos de patch e remover a linha inGroups
    for line in lines:
        stripped = line.strip()

        # Detecta o início de um patch
        if stripped in boundary_types:
            inside_patch = True
            current_patch = stripped
            corrected_lines.append(line)
            continue

        # Remove a linha 'inGroups' se estiver dentro de um patch
        if "inGroups" in stripped:
            continue

        # Corrige o tipo de fronteira se estiver dentro de um patch
        if inside_patch and "type" in stripped:
            corrected_lines.append(f"        type            {boundary_types[current_patch]};\n")
            inside_patch = False  # Sai do patch após modificar
            continue

        # Continua copiando as linhas normalmente
        corrected_lines.append(line)

    # Escrever o novo arquivo boundary corrigido
    with open(boundary_file, "w") as file:
        file.writelines(corrected_lines)

    logger.info(f"Arquivo boundary corrigido com sucesso em {case_folder}. Backup salvo em {backup_file}")
    return True
