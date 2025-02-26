import os
import shutil


def fix_boundary(case_dir):
    """
    Corrige os tipos de fronteira no arquivo boundary do OpenFOAM.

    Args:
        case_dir (str): Caminho do diretório do caso.
    """
    boundary_file = os.path.join(case_dir, "constant/polyMesh/boundary")
    backup_file = boundary_file + ".bk"

    if not os.path.exists(boundary_file):
        print(f"Aviso: Arquivo boundary não encontrado em {case_dir}.")
        return

    # Criar backup antes da modificação
    if not os.path.exists(backup_file):
        shutil.copy(boundary_file, backup_file)

    # Ler o arquivo boundary
    with open(boundary_file, "r") as file:
        lines = file.readlines()

    # Dicionário com os tipos corretos de fronteira
    boundary_types = {
        "inlet": "patch",
        "outlet": "patch",
        "top": "patch",
        "bottom": "patch",
        "front": "empty",
        "back": "empty",
        "wall": "wall",
    }

    corrected_lines = []
    inside_patch = False
    current_patch = ""

    for line in lines:
        stripped = line.strip()

        if stripped in boundary_types:
            inside_patch = True
            current_patch = stripped
            corrected_lines.append(line)
            continue

        if inside_patch and "type" in stripped:
            corrected_lines.append(
                f"        type            {boundary_types[current_patch]};\n"
            )
            inside_patch = False
            continue

        if "inGroups" in stripped:
            continue  # Remove a linha 'inGroups'

        corrected_lines.append(line)

    # Escrever o arquivo boundary corrigido
    with open(boundary_file, "w") as file:
        file.writelines(corrected_lines)

    print(f"Boundary corrigido em: {boundary_file}")
