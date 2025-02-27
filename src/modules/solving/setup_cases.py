import os
import shutil


def create_case_directories(base_mesh_dir, base_case_dir):
    """
    Cria as pastas de caso correspondentes às malhas geradas.
    """
    mesh_cases = [
        d
        for d in os.listdir(base_mesh_dir)
        if os.path.isdir(os.path.join(base_mesh_dir, d))
    ]

    if not mesh_cases:
        print(
            " Nenhuma malha encontrada em 'meshes/'. Verifique se a geração da malha foi executada."
        )

    for case in mesh_cases:
        case_path = os.path.join(base_case_dir, case)
        if not os.path.exists(case_path):
            os.makedirs(case_path)
            print(f" Pasta criada: {case_path}")
        else:
            print(f"🔹 Pasta já existente: {case_path}")


def copy_template_files(template_dir, base_case_dir):
    """
    Copia os arquivos de template para cada pasta de caso.
    """
    case_dirs = [
        d
        for d in os.listdir(base_case_dir)
        if os.path.isdir(os.path.join(base_case_dir, d))
    ]

    if not os.path.exists(template_dir):
        print(f" ERRO: Diretório de template '{template_dir}' não encontrado!")
        return

    for case in case_dirs:
        case_path = os.path.join(base_case_dir, case)

        for item in os.listdir(template_dir):
            src_item = os.path.join(template_dir, item)
            dest_item = os.path.join(case_path, item)

            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy(src_item, dest_item)

        print(f" Templates copiados para {case_path}")


def link_polyMesh(base_mesh_dir, base_case_dir):
    """
    Cria links simbólicos para a malha dentro da pasta de cada caso.
    """
    mesh_cases = [
        d
        for d in os.listdir(base_mesh_dir)
        if os.path.isdir(os.path.join(base_mesh_dir, d))
    ]

    for case in mesh_cases:
        mesh_polyMesh_path = os.path.join(base_mesh_dir, case, "constant", "polyMesh")
        case_polyMesh_path = os.path.join(base_case_dir, case, "constant", "polyMesh")

        if os.path.exists(mesh_polyMesh_path):
            os.makedirs(os.path.dirname(case_polyMesh_path), exist_ok=True)
            os.system(f"ln -sf {mesh_polyMesh_path} {case_polyMesh_path}")
            print(f"🔗 Link simbólico criado: {case_polyMesh_path}")
        else:
            print(f"⚠ Aviso: Malha não encontrada para {case}")


def setup_cases():
    """
    Configura todos os casos de simulação com base nas malhas existentes.
    """
    base_mesh_dir = os.path.join(os.getcwd(), "meshes")
    base_case_dir = os.path.join(os.getcwd(), "cases")
    template_dir = os.path.join(os.getcwd(), "templates", "simplefoam")

    print("\n Iniciando configuração das pastas de simulação...\n")

    create_case_directories(base_mesh_dir, base_case_dir)
    copy_template_files(template_dir, base_case_dir)
    link_polyMesh(base_mesh_dir, base_case_dir)

    print("\nConfiguração concluída!\n")


if __name__ == "__main__":
    setup_cases()
