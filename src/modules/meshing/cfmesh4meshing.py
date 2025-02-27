import os
import shutil

# -------------------------------------------------------- #
from modules.meshing.running_mesh import configure_mesh, execute_mesh


# -------------------------------------------------------- #
def meshing():
    """
    Configura e gera malhas para todos os arquivos STL na pasta geometries/merged.
    """
    base_dir = os.getcwd()
    merged_dir = os.path.join(base_dir, "geometries", "merged")
    template_dir = os.path.join(base_dir, "templates", "cfmesh")
    base_meshes_dir = os.path.join(base_dir, "meshes")

    # Limpa a pasta meshes para evitar aninhamento excessivo
    if os.path.exists(base_meshes_dir):
        shutil.rmtree(base_meshes_dir)

    os.makedirs(base_meshes_dir, exist_ok=True)  # Recria estrutura vazia

    # Verifica se o template existe
    if not os.path.exists(template_dir):
        print(f"Erro: O diretório de template '{template_dir}' não existe!")
        return

    # Processa apenas arquivos STL
    for file in os.listdir(merged_dir):  # Testa apenas dois casos inicialmente
        if file.endswith(".stl"):
            case_name = f"case_{file[:-4]}"  # Remove extensão

            # Configurar a malha
            configure_mesh(case_name, template_dir, merged_dir)

            # Executar o comando cartesianMesh
            execute_mesh(case_name)


# Call the meshing function to start the process
# meshing()
