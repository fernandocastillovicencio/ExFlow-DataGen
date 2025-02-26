import os
import shutil
import subprocess

# -------------------------------------------------------- #
from modules.meshing.fix_boundaries import fix_boundary

# -------------------------------------------------------- #


def configure_mesh(case_name, template_dir, merged_dir):
    """
    Configura a malha copiando arquivos de template para o diretório do caso
    e movendo o arquivo STL para o local correto.

    Args:
        case_name (str): Nome do caso (ex: 'case_001').
        template_dir (str): Caminho para o diretório contendo arquivos de sistema.
        merged_dir (str): Caminho para o diretório contendo os arquivos STL mesclados.
    """
    base_meshes_dir = os.path.join(os.getcwd(), "meshes")
    case_dir_meshes = os.path.join(base_meshes_dir, case_name)  # Correção do caminho
    constant_dir = os.path.join(case_dir_meshes, "constant", "triSurface")

    # Limpar diretório do caso antes de recriar
    if os.path.exists(case_dir_meshes):
        shutil.rmtree(case_dir_meshes)

    # Criar estrutura correta
    os.makedirs(constant_dir, exist_ok=True)

    # Copiar arquivos de template
    if os.path.exists(template_dir):
        for item in os.listdir(template_dir):
            src_item = os.path.join(template_dir, item)
            dest_item = os.path.join(case_dir_meshes, item)
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy(src_item, dest_item)
    else:
        print(f"Erro: O diretório de template '{template_dir}' não existe!")

    # Copiar o arquivo STL correspondente
    stl_file = f"{case_name[5:]}.stl"  # Retira o prefixo 'case_'
    stl_src = os.path.join(merged_dir, stl_file)

    if os.path.exists(stl_src):
        stl_dest = os.path.join(constant_dir, "geom.stl")
        shutil.copy(stl_src, stl_dest)
        print(f"STL copiado e renomeado para: {stl_dest}")
    else:
        print(f"Aviso: Arquivo STL {stl_src} não encontrado!")


# -------------------------------------------------------- #


# -------------------------------------------------------- #
def extrudeMesh(method="single"):
    if method == "single":
        # Executar o comando cartesianMesh
        subprocess.run("extrudeMesh > log.extrudeMesh", shell=True, check=True)
    else:
        subprocess.run(
            """
        decomposePar > log.decomposePar
        mpirun -np 12 extrudeMesh -parallel > log.cartesianMesh
        reconstructPar -constant > log.reconstructPar
        rm -rf processor* 
        """,
            shell=True,
            check=True,
        )


# -------------------------------------------------------- #


def execute_mesh(case_name):
    """
    Executa o comando cartesianMesh para um caso específico.

    Args:
        case_name (str): Nome do caso (ex: 'case_001').
    """
    base_dir = os.getcwd()
    case_dir_meshes = os.path.join(base_dir, "meshes", case_name)

    if not os.path.exists(case_dir_meshes):
        print(f"Erro: O diretório {case_dir_meshes} não existe.")
        return

    try:
        os.chdir(case_dir_meshes)
        print(f"Executando malha em: {case_dir_meshes}")

        # Descomentar para execução real do cartesianMesh
        subprocess.run("cartesianMesh > log.cartesianMesh", shell=True, check=True)
        # ------------------ extrudemesh ----------------- #
        extrudeMesh("single")
        # ------------------------------------------------ #
        subprocess.run("checkMesh > log.checkMesh", shell=True, check=True)
        # ------------------------------------------------ #
        subprocess.run("touch case.foam", shell=True, check=True)
        print(f"Malha gerada com sucesso para: {case_name}")

        # ------------------------------------------------ #
        # Corrigir boundary
        fix_boundary(case_dir_meshes)
        print(f"Malha gerada e corrigida para: {case_name}")

    except Exception as e:
        print(f"Erro ao executar cartesianMesh: {e}")

    finally:
        os.chdir(base_dir)  # Retorna ao diretório original
